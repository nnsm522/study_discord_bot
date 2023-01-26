import pandas as pd

def load_file(file_name):
    data = pd.read_csv(f"data/{file_name}.csv")
    data.set_index('discord id', inplace=True)
    return data

df = load_file("member_info")

if df is not None :
    print("hi")