import os 
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(".env")

# load environment variables
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOSTNAME = "localhost"
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_PORT = 27017

DATABASE_CONNECTION_URI=f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}:{MONGODB_PORT}/{MONGODB_DATABASE}"
print(DATABASE_CONNECTION_URI)
# Database 
client = MongoClient(DATABASE_CONNECTION_URI)
db = client[MONGODB_DATABASE]
call_collection = db['calls']

print(call_collection)
import json
data_json = json.load(open("test.json", "r"))
# print(data_json)

for data in data_json:
    print(data)
    number = data
    sent = data_json[data]["sent"]
    received = data_json[data]["received"]
    print(sent, received)
    call_collection.insert_one({"number": number, "sent": sent, "received": received})