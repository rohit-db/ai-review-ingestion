# Databricks notebook source
# MAGIC %pip install -U openai pandas dbtunnel[gradio] dspy-ai pydantic
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ./00_CONFIG

# COMMAND ----------

from auto_topic.domains import DomainConfigTable
from auto_topic.sentiment import get_analyzer, enable_arize_tracing, get_valid_responses_for_categories
import pandas as pd

# COMMAND ----------

dct = DomainConfigTable.from_table(spark, catalog=CATALOG, schema=SCHEMA, table=QUESTIONS_TABLE)

# COMMAND ----------

import dspy
TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
topics_df = pd.DataFrame([topic.to_kwargs() for topic in dct.topics])

# COMMAND ----------

topics_df

# COMMAND ----------

from pyspark.sql import functions as F
import json
import dspy

from typing import Iterator, Tuple

@F.pandas_udf("string")
def extract_domain_details(feedback_and_ratings: Iterator[Tuple[pd.Series, pd.Series]]) -> Iterator[pd.Series]:
    # Do some expensive initialization with a state
    language_model = dspy.OpenAI(
        model='databricks-meta-llama-3-70b-instruct', # model='databricks-dbrx-instruct',
        max_tokens=500,
        temperature=0.1,
        api_key=TOKEN,
        api_base="https://e2-demo-field-eng.cloud.databricks.com/serving-endpoints/"
    )
    extract = get_analyzer(topics_df, language_model)
    for feedback_arr, rating_arr in feedback_and_ratings:
        # Use that state for whole iterator.
        feedbacks, ratings = feedback_arr.tolist(), rating_arr.tolist()
        results = []
        for feedback, rating in zip(feedbacks, ratings):
            resp = extract(feedback=feedback, rating=str(rating))
            final_resp = json.dumps({"category_breakdown": resp.breakdown.to_dict(), 
                    "category_selection": resp.category_selection,
                    "category_selection_rationale": resp.category_selection_rationale,
                    "all_categories": get_valid_responses_for_categories(topics_df)})
            results.append(final_resp)

        yield pd.Series(results)
  


# COMMAND ----------

reviews = spark.table(f"{CATALOG}.{SCHEMA}.{REVIEWS_TABLE}")
reviews.display()
reviews = reviews.limit(1)

# COMMAND ----------

# write target table

reviews = reviews.withColumn("analysis", extract_domain_details("review", "rating"))
reviews.display()

# COMMAND ----------

if spark.catalog.tableExists(f"{CATALOG}.{SCHEMA}.{TARGET_TABLE}") is False:
    print(f"Creating Target Table: {CATALOG}.{SCHEMA}.{TARGET_TABLE}")
    # todo remove limit 10
    spark.sql(f"""
              SELECT *, cast(null as string) as analysis FROM {CATALOG}.{SCHEMA}.{REVIEWS_TABLE}
              limit 10
              """).write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.{SCHEMA}.{TARGET_TABLE}")
else:
    print(f"Table: {CATALOG}.{SCHEMA}.{TARGET_TABLE} already exists!")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- seed reviews
# MAGIC SELECT * FROM main.sri_winedb.reviews_predictions;

# COMMAND ----------

from delta.tables import DeltaTable

target_table = DeltaTable.forName(spark, f"{CATALOG}.{SCHEMA}.{TARGET_TABLE}")

records = spark.sql(f"SELECT *, cast(null as string) as analysis FROM {CATALOG}.{SCHEMA}.{REVIEWS_TABLE}")

target_table.alias("target").merge(
    source=records.alias("source"),
    condition="target.review_id = source.review_id",

).whenNotMatchedInsertAll().execute()

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY main.sri_winedb.reviews_predictions;

# COMMAND ----------

from delta.tables import DeltaTable

BATCH_SIZE = 5

def get_unanalyzed_records(spark, batch_size = None):
    if batch_size is None:
        return spark.table(f"{CATALOG}.{SCHEMA}.{TARGET_TABLE}").where("analysis is null")
    else:
        return spark.table(f"{CATALOG}.{SCHEMA}.{TARGET_TABLE}").where("analysis is null").limit(batch_size)

unanalyzed_records = get_unanalyzed_records(spark, BATCH_SIZE)
unanalyzed_records_ct = unanalyzed_records.count()
unanalyzed_records_ct
batch_ct = 1
while unanalyzed_records_ct > 0:
    print(f"Analyzing {unanalyzed_records_ct} records...; batch number {batch_ct}")
    analyzed_records = unanalyzed_records.withColumn("analysis", extract_domain_details("review", "rating"))
    target_table = DeltaTable.forName(spark, f"{CATALOG}.{SCHEMA}.{TARGET_TABLE}")
    target_table.alias("target").merge(
        source=analyzed_records.alias("source"),
        condition="target.review_id = source.review_id",
    ).whenMatchedUpdateAll().execute()

    # fetch new batch
    unanalyzed_records = get_unanalyzed_records(spark, BATCH_SIZE)
    unanalyzed_records_ct = unanalyzed_records.count()
    batch_ct += 1




# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM main.sri_winedb.reviews_predictions;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE main.sri_winedb.reviews_predictions set analysis = null where analysis:category_breakdown:error is not null;

# COMMAND ----------


