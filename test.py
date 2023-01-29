import pymongo
import os
from dotenv import load_dotenv



load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')

mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client.member

def update_member_data(discord_id, discord_name,
        name, birth, school, personal_phone_number, parents_phone_number,
        exam_grades=[None, None, None, None, None, None, None, None, None, None, None, None],
        r_coin=0):
    global db
    key = {"discord_id": discord_id}
    data = {
        "discord_id": discord_id,
        "discord_name": discord_name,
        "이름": name,
        "생년월일": birth,
        "학교": school,
        "개인_연락처": personal_phone_number,
        "부모님_연락처": parents_phone_number,
        "성적": {
            "1-1중간": exam_grades[0],
            "1-1기말": exam_grades[1],
            "1-2중간": exam_grades[2],
            "1-2기말": exam_grades[3],
            "2-1중간": exam_grades[4],
            "2-1기말": exam_grades[5],
            "2-2중간": exam_grades[6],
            "2-2기말": exam_grades[7],
            "3-1중간": exam_grades[8],
            "3-1기말": exam_grades[9],
            "3-2중간": exam_grades[10],
            "3-2기말": exam_grades[11],
        },
        "r_coin": r_coin
    }
    try:
        db.member_data.update_one(key, {"$set": data}, True)
    except Exception as e:
        print(f"error: {e}")
    else:
        print("DB update Success!")

update_member_data(1058626232431951912, "테스트#1234", "장연철", "950522", "난우중", "010-9452-5774", "010-9034-1448")


a = db.member_data.find_one({"discord_id": 1058626232431951912})

print(a["성적"])

def k(a=2, b=3):
    print(a)
    print(b)
    print(a+b)

k(a=None, b=1)