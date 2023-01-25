import pandas as pd

student_info_data = {'discord id': ["'1058626232431951912"], 'discord name' : ["장연철#6966"], '이름' : ["장연철"], '생년월일' : ["`950522"], '학교' : ["난우중학교"], '연락처' : ["010-9452-5774"]}
exam_grades_data = {'discord id': ["'1058626232431951912"], '1-1중간' : [50], '1-1기말' : [50], '1-2중간' : [50], '1-2기말' : [50], '2-1중간' : [50], '2-1기말' : [50], '2-2중간' : [50], '2-2기말' : [50], '3-1중간' : [50], '3-1기말' : [50], '3-2중간' : [50], '3-2기말' : [50]}

student_info = pd.DataFrame(student_info_data)
exam_grades = pd.DataFrame(exam_grades_data)
student_info.set_index('discord id', inplace=True)
exam_grades.set_index('discord id', inplace=True)


a = student_info.loc["'1058626232431951912"]
print(a["discord name"])