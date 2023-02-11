import os
from dotenv import load_dotenv
import pymongo

load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')

mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client.member

data = db.member_data.find_one({"discord_id": 1058626232431951912})

mongo_client.close()
print(data)