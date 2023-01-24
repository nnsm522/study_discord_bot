import pandas as pd

data = {'custom_id': '63c990ca519cd430c0af55dc46c75ac5',
        'components': [{'type': 1, 'components': [{'value': '장연철', 'type': 4, 'custom_id': '609bc595f25d831bd764f66402a2756b'}]},
                        {'type': 1, 'components': [{'value': '950522', 'type': 4, 'custom_id': '0ef26810b8e8654b11583c7e85489c6b'}]}, 
                        {'type': 1, 'components': [{'value': '중중중', 'type': 4, 'custom_id': '6d04761e70b8b6ce93eb547840b47560'}]}, 
                        {'type': 1, 'components': [{'value': '010-9452-5774', 'type': 4, 'custom_id': '817eb7601800f12edef74dd7800a66dc'}]}, 
                        {'type': 1, 'components': [{'value': '010-9034-1448', 'type': 4, 'custom_id': '9b8c3622db197beacf82a96da44cbd62'}]}
                        ]
        }


student_info_data = {'discord id': ["'1058626232431951912"], 'discord name' : ["장연철#6966"], '이름' : ["장연철"], '생년월일' : ["`950522"], '학교' : ["난우중학교"], '연락처' : ["010-9452-5774"]}
exam_grades_data = {'discord id': ["'1058626232431951912"], '1-1중간' : [50], '1-1기말' : [50], '1-2중간' : [50], '1-2기말' : [50], '2-1중간' : [50], '2-1기말' : [50], '2-2중간' : [50], '2-2기말' : [50], '3-1중간' : [50], '3-1기말' : [50], '3-2중간' : [50], '3-2기말' : [50]}

student_info = pd.DataFrame(student_info_data)
exam_grades = pd.DataFrame(exam_grades_data)
student_info.set_index('discord id', inplace=True)
exam_grades.set_index('discord id', inplace=True)


student_info.to_csv("./data/student_info.csv", encoding='utf-8-sig')
exam_grades.to_csv("./data/exam_grades.csv", encoding='utf-8-sig')


