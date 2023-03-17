import os
from dotenv import load_dotenv
import pymongo

load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')
GUILD_ID = os.getenv('GUILD_ID')

def import_member_data(discord_id):
    try:
        mongo_client = pymongo.MongoClient(MONGO_URL)
        db = mongo_client.member
        data = db.member_data.find_one({"discord_id": discord_id})
    except Exception as e:
        print(e)
    else:
        mongo_client.close()
        return data
    
def update_member_data(data:dict):
    key = {"discord_id": data["discord_id"]}
    try:
        mongo_client = pymongo.MongoClient(MONGO_URL)
        db = mongo_client.member
        db.member_data.update_one(key, {"$set": data}, True)
    except Exception as e:
        print(f"error: {e}")
    else:
        mongo_client.close()
        print("Member data update Success!")

def delete_member_data(discord_id):
    try:
        mongo_client = pymongo.MongoClient(MONGO_URL)
        db = mongo_client.member
        db.member_data.delete_one({"discord_id": discord_id})
    except Exception as e:
        print(f"error: {e}")
    else:
        mongo_client.close()
        print(f"Member data delete Success!")

def member_data_model(
        discord_id:str=None,
        discord_name:str=None,
        name:str=None,
        birth:str=None,
        school:str=None,
        parents_phone_number:str=None,
        email:str=None,
        exam_grades:dict={
            "중1-1중간": None,
            "중1-1기말": None,
            "중1-2중간": None,
            "중1-2기말": None,
            "중2-1중간": None,
            "중2-1기말": None,
            "중2-2중간": None,
            "중2-2기말": None,
            "중3-1중간": None,
            "중3-1기말": None,
            "중3-2중간": None,
            "중3-2기말": None,
        },
        r_coin:int=0,
):
    data = {
        "discord_id": discord_id,
        "discord_name": discord_name,
        "이름": name,
        "생년월일": birth,
        "학교": school,
        "부모님_연락처": parents_phone_number,
        "이메일": email,
        "성적": exam_grades,
        "r_coin": r_coin,
    }
    return data


def update_token(discord_id, creds):
    try:
        mongo_client = pymongo.MongoClient(MONGO_URL)
        db = mongo_client.member
        db.member_data.update_one({"discord_id": discord_id}, {"$set": {"token": creds.to_json()}}, True)
    except Exception as e:
        print(f"error: {e}")
    else:
        mongo_client.close()
        print(f"token update Success!")
    

