import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import db_module

SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
'https://www.googleapis.com/auth/classroom.rosters',
'https://www.googleapis.com/auth/classroom.profile.emails',
'https://www.googleapis.com/auth/classroom.profile.photos',
'https://www.googleapis.com/auth/classroom.coursework.students']


def check_token(discord_id):
    data = db_module.import_member_data(discord_id)
    token = None if data is None else data["token"]
    creds = None

    if token:
        creds = Credentials.from_authorized_user_info(eval(token), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            db_module.update_token(discord_id, creds)
    
    return creds
    

# course_id = '592792151291'
# enrollment_code = 'olagxrj'
# student = {'userId' : 'jangyc95@gmail.com'}
# try:
#     service = build('classroom', 'v1', credentials=creds)
#     students = service.courses().students().list(courseId=course_id).execute()
#     print(students)
# except HttpError as error:
#     print('An error occurred: %s' % error)

def get_course_list(discord_id):
    creds = check_token(discord_id)
    try:
        service = build('classroom', 'v1', credentials=creds)
        courses = []
        page_token = None

        while True:
            # pylint: disable=maybe-no-member
            response = service.courses().list(pageToken=page_token,
                                              pageSize=100).execute()
            courses.extend(response.get('courses', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not courses:
            print("No courses found.")
            return
        print("Courses:")
        for course in courses:
            print(f"{course.get('name'), course.get('id')}")
        return courses
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error



if __name__ == "__main__":
    a = get_course_list('1234567890')
    print(a)