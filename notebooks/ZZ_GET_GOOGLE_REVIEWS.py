# Databricks notebook source
# MAGIC %md
# MAGIC # Enable Places API & Get Google API Key
# MAGIC **Enable the Places API**
# MAGIC In the Google Cloud Console, navigate to APIs & Services > Library, and search for Places API.
# MAGIC
# MAGIC **Get an API Key**
# MAGIC After enabling the API, go to APIs & Services > Credentials, and create an API key.

# COMMAND ----------

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

scope_name = 'rohitb_demo'
try:
  w.secrets.create_scope(scope=scope_name)
except Exception as e:
  print(e)

# w.secrets.put_secret(scope=scope_name, key='google_api_key', string_value='<token>')

# COMMAND ----------

# MAGIC %run ./00_CONFIG

# COMMAND ----------

import requests
import csv
import time

API_KEY = dbutils.secrets.get(scope='rohitb_demo', key='google_api_key')

# COMMAND ----------

def get_place_ids(query, location, radius):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&key={API_KEY}"
    response = requests.get(url)
    places = response.json().get('results', [])
    place_details = [(place['place_id'], place['name'], place['formatted_address']) for place in places]
    return place_details

def get_reviews(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}'
    response = requests.get(url)
    reviews = response.json().get('result', {}).get('reviews', [])
    return reviews

def fetch_reviews_for_all_places(query, location, radius):
    place_details = get_place_ids(query, location, radius)
    all_reviews = []

    for place_id, name, address in place_details:
        reviews = get_reviews(place_id)
        for review in reviews:
            all_reviews.append([place_id, name, address, review['author_name'], review['rating'], review['text'], review['relative_time_description']])
        time.sleep(2)  # Pause to respect API rate limits

    return all_reviews

# COMMAND ----------

# Define parameters for the search
query = 'Advance Auto Parts'
location = '39.000000,-75.500000.'  # Latitude and Longitude for Delaware
radius = 100000  # Radius in meters (10km)

# Fetch reviews for all locations
all_reviews = fetch_reviews_for_all_places(query, location, radius)

# COMMAND ----------

# List of top 10 cities in the US with their latitude and longitude
cities = [
    ('New York', '40.712776,-74.005974'),
    ('Los Angeles', '34.052235,-118.243683'),
    ('Chicago', '41.878113,-87.629799'),
    ('Houston', '29.760427,-95.369804'),
    ('Phoenix', '33.448376,-112.074036'),
    ('Philadelphia', '39.952583,-75.165222'),
    ('San Antonio', '29.424122,-98.493629'),
    ('San Diego', '32.715736,-117.161087'),
    ('Dallas', '32.776665,-96.796989'),
    ('San Jose', '37.338207,-121.886330')
]

# Define parameters for the search
# query = 'Little Caesars'

query = 'Pilot Flying J'
radius = 20000  # Radius in meters (20km)

# Initialize an empty list to store all reviews
all_reviews = []

# Loop through each city to fetch reviews
for city, location in cities:
    city_reviews = fetch_reviews_for_all_places(query, location, radius)
    all_reviews.extend(city_reviews)

# COMMAND ----------

from pyspark.sql.functions import current_date, monotonically_increasing_id

df = spark.createDataFrame(all_reviews, ['place_id', 'name', 'address', 'author', 'rating', 'review', 'time'])
df = df.withColumn('load_date', current_date()).withColumn('review_id', monotonically_increasing_id())
df.display()

# COMMAND ----------

# MAGIC %sql 
# MAGIC

# COMMAND ----------

df.write.mode('overwrite').saveAsTable(f'rohitb_demo.lce_demo.reviews')

# COMMAND ----------

# MAGIC %md
# MAGIC # Latitude & Longitude

# COMMAND ----------



# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, DoubleType
# List of addresses

addresses = [row['address'] for row in spark.sql("select distinct address from rohitb_demo.kfc_demo.dim_stores").collect()]


# Create a DataFrame from the list of addresses
schema = StructType([StructField("address", StringType(), True)])
address_df = spark.createDataFrame([(addr,) for addr in addresses], schema)

# Define a function to fetch latitude and longitude using requests
def fetch_coordinates(address):
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print(f"Geocoding error for address '{address}': {data['status']}")
                return None, None
        else:
            print(f"HTTP error: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None

# Register the function as a UDF
fetch_coordinates_udf = udf(
    lambda addr: fetch_coordinates(addr),
    StructType([
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True)
    ])
)

# Apply the UDF to the DataFrame
geocoded_df = address_df.withColumn("coordinates", fetch_coordinates_udf(address_df["address"]))

# Split the coordinates into separate latitude and longitude columns
final_df = geocoded_df.select(
    "address",
    geocoded_df["coordinates.latitude"].alias("latitude"),
    geocoded_df["coordinates.longitude"].alias("longitude")
)


# COMMAND ----------

API_KEY

# COMMAND ----------

fetch_coordinates('1922 3rd Ave, Manhattan, NY 10029, United States')

# COMMAND ----------

geocoded_df.display()

# COMMAND ----------

geocoded_df.display()

# COMMAND ----------


