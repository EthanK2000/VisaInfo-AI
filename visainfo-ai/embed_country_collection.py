from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from openai import OpenAI
import os
import argparse

def embed_country_collecton():
    client = MongoClient(os.environ['MONGODB_ATLAS_URI'], server_api=ServerApi('1'))
    clientOpenAI = OpenAI()
    database = client["VisaInfo-Database"]
    collection = database["Country"]
    cursor = collection.find({})
    for document in cursor:
        if "embedding_vector" not in document:
            country = document["country"]
            print(f"Updating embedding for {country}...")
            text_embedding = ", ".join([document["country"], document["nationality"], document["code"]])
            if "alias" in document:
                text_embedding = text_embedding + ", " + ", ".join(document["alias"])
            embedding = clientOpenAI.embeddings.create(input=text_embedding, model=os.environ['OPEN_AI_EMBEDDING_MODEL']).data[0].embedding
            query_filter = {"_id" : document["_id"]}
            update_operation = { "$set" : 
                { "embedding_vector" : embedding }
            }
            collection.update_one(query_filter, update_operation)
    return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog='Embed Country Collection',
                description='Create vector embeddings for countries.')
    print(f"Embedding new countries vectors...")
    embed_country_collecton()
    print(f"Done embedding new countries vectors.")
    