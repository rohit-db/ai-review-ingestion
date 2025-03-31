# Databricks notebook source
# MAGIC %pip install bertopic
# MAGIC %pip install -U openai
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ./00_CONFIG

# COMMAND ----------

REVIEWS_TABLE = 'costa_google_reviews'
reviews_df = spark.table(f"{CATALOG}.{SCHEMA}.{REVIEWS_TABLE}").toPandas()

# COMMAND ----------

all_reviews = reviews_df["review"].tolist()

# COMMAND ----------

from transformers import AutoModel, AutoTokenizer

# Download and cache the model locally
model = AutoModel.from_pretrained("thenlper/gte-large")
tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")


# COMMAND ----------

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, OpenAI
import openai

# You can bootstrap with basic topics that you may want to pull
# Try picking relevant topics that you want your data clustered to
# you can also split up the parent review into sentence chunks and associate sentences to topics to be able to map a single review to one of these topics
# zeroshot_topic_list = ["Good Movie", "Bad Movie", "Good Game", "Bad Game", "Other", "Defect Issues Not Working", "Gifts"]

zeroshot_topic_list = [
    "Customer Service", "Coffee Quality", "Food Quality", "Ambiance", 
    "Hygiene and Cleanliness", "Seating and Space", "Wi-Fi and Connectivity", "Queue Management and Speed", 
    "Staff Attitude and Behavior", "Special Promotions and Offers", "Out-of-Stock Items", 
    "Customer Satisfaction", "Health and Safety Concerns"
]



# Reference: https://maartengr.github.io/BERTopic/getting_started/zeroshot/zeroshot.html#example
# if you are doing this with a lot of data you may want to use a gpu to use the embedding model otherwise 
# this can run for a while

TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
client = openai.OpenAI(base_url=f"{WORKSPACE_URL}/serving-endpoints/", api_key=TOKEN)
openai_generator = OpenAI(client, model=MODEL_ID)

ai_representation = [MaximalMarginalRelevance(diversity=0.4), openai_generator]

representations = {
    "AiBased": ai_representation,
    "KeyBERT": KeyBERTInspired()
}

topic_model = BERTopic(
    # embedding_model="thenlper/gte-large", # use thenlper/gte-large or thenlper/gte-small; use small if you want this to run fast
    embedding_model = model,
    min_topic_size=15,
    zeroshot_topic_list=zeroshot_topic_list,
    zeroshot_min_similarity=.85,
    representation_model=representations # see if there is a better representation model
)
topics, _ = topic_model.fit_transform(all_reviews)

# COMMAND ----------

spark.createDataFrame(topic_model.get_topic_info()).display()

# COMMAND ----------

topic_distr, _ = topic_model.approximate_distribution(["I'd like to sincerely thank Mariam for her kindness and speedy service. She told me that they're unable to serve iced coffee at the moment and I was okay with a hot drink as well but she insisted to offer it on the house knowing that I didn't come for a hot drink. Bless her, for me it's not the free coffee but it is personally a treat to come across thoughtful and smiling employees that care about the customers with a genuine caring attitude regardless of the company they're working at. I wanted to spend the time to write this comment hoping that she'd appreciate it but also so that it can be a great example for other people that come across it."])
topic_distr

# COMMAND ----------

topic_model.visualize_distribution(topic_distr[0])

# COMMAND ----------

new_document_topic, topic_probabilities = topic_model.transform(["Ridiculous service from the barista lady at this store on a Friday afternoon. I’ve just ordered a berry infusion tea where it clearly stated on the menu board, ONLY medium size available. Instead of a medium paper cup she deliberately gave me a small cup with the tea. I came up asking if it’s the correct size, she even tried to make it up by asking me back:” Which one you like? Small or medium. It’s the same price.”I mean, huh? Are you being serious? When you order tea at a cafe what size would you normally expect? You paid £2.65 for a small? Even a medium would be just a few more drops of water! I’m not the first time ordering from Costa. The second I hold the tea I knew immediately it’s the wrong size. And no apologies nothing! Is this whole thing even making sense??\nThe photo below is the correct size I got after questioning at the counter. LOL! Disgusting"])
# Get the topic ID assigned to the new document
topic_id = new_document_topic[0]
# Get the topic words for the assigned topic
topic_words = topic_model.get_topic(topic_id)
topic_string = ", ".join([word for word, _ in topic_words])
print(f"The new document is related to Topic {topic_id}: {topic_string}")
print(topic_probabilities)

# COMMAND ----------

import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters
    text = re.sub(r'\W+', ' ', text)
    # Remove stopwords
    text = " ".join([word for word in text.split() if word not in ENGLISH_STOP_WORDS])
    return text


# COMMAND ----------

new_document = preprocess_text("Ridiculous service from the barista lady at this store on a Friday afternoon. I’ve just ordered a berry infusion tea where it clearly stated on the menu board, ONLY medium size available. Instead of a medium paper cup she deliberately gave me a small cup with the tea. I came up asking if it’s the correct size, she even tried to make it up by asking me back: 'Which one you like? Small or medium. It’s the same price.' I mean, huh? Are you being serious? When you order tea at a cafe what size would you normally expect? You paid £2.65 for a small? Even a medium would be just a few more drops of water! I’m not the first time ordering from Costa. The second I hold the tea I knew immediately it’s the wrong size. And no apologies nothing! Is this whole thing even making sense?? The photo below is the correct size I got after questioning at the counter. LOL! Disgusting")

new_document_topic, topic_probabilities = topic_model.transform([new_document])

# Get the topic ID assigned to the new document
topic_id = new_document_topic[0]
# Get the topic words for the assigned topic
topic_words = topic_model.get_topic(topic_id)
topic_string = ", ".join([word for word, _ in topic_words])
print(f"The new document is related to Topic {topic_id}: {topic_string}")
print(topic_probabilities)


# COMMAND ----------

topic_model.transform([new_document])

# COMMAND ----------


