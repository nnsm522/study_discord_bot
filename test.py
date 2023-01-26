import pandas as pd

def load_file(file_name):
    data = pd.read_csv(f"data/{file_name}.csv")
    data.set_index('discord id', inplace=True)
    return data

df = load_file("member_info")

print(type(df.loc[f"'1058626232431951912"]["이름"]))