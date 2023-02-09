import os
from dotenv import load_dotenv
import pymongo

load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')

mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client.member
last_member_data = None

print(mongo_client.member.member_data.find_one({"discord_id": 1058626232431951912}) is not None)

