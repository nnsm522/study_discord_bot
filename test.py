import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import pymongo

load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')

mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client.member

#data = db.member_data.find_one({"discord_id": 1058626232431951912})

#mongo_client.close()

SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
'https://www.googleapis.com/auth/classroom.rosters',
'https://www.googleapis.com/auth/classroom.profile.emails',
'https://www.googleapis.com/auth/classroom.profile.photos',
'https://www.googleapis.com/auth/classroom.coursework.students']


token = db.member_data.find_one({"discord_id": '12345678'})['token']
creds = None

if token:
    creds = Credentials.from_authorized_user_info(eval(token), SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        db.member_data.update_one({"discord_id": '12345678'}, {"$set": {"token": creds.to_json()}}, True)

course_id = '592792151291'
enrollment_code = 'olagxrj'
student = {'userId' : 'jangyc95@gmail.com'}
try:
    service = build('classroom', 'v1', credentials=creds)
    students = service.courses().students().list(courseId=course_id).execute()
    print(students)
except HttpError as error:
    print('An error occurred: %s' % error)