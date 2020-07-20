import numpy as np
import pandas as pd
from datetime import datetime
from flask import Flask, url_for
import json
import time
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def default():
    return "Server 2!"

@app.route("/parse")
def parse():
    with open('data.json') as json_file:
        jdata = json.load(json_file)
        return (executeData(jdata))


def executeData(data):
    party_dict = {
    'Democratic-Republican': 'DR', 
    'Democrat': 'DEM', 'Whig': 'WH', 'Republican': 'REP', 
    'National Union': 'NU'
    }
    # JSON to DataFrame
    df = pd.DataFrame(data)

    # Transforming date into 'From' and 'To' year
    df[['From', 'To']] = df.tm.str.split("-", expand=True)
    df['From'] = df['From'].astype(str).astype(int)

    def centuryFromYear(year):
        return (year // 100 + 1)  # 1 because 2017 is 21st century, and 1989 = 20th century

    df['Century'] = centuryFromYear(df['From'])
    
    # dropping rows of Federalist
    df = df[~df['pp'].str.contains('Federalist')]
    
    # Extracting FirstName and reversing
    df[['FirstName', 'SecondName', 'ThirdName', 'FourthName']] = df.nm.str.split(" ", expand=True)
    df['FirstName'] = df['FirstName'].astype(str)
    df['Name'] = df['FirstName'].apply(lambda x: x[::-1])
    
    # Sorting the DataFrame by Century and FirstName
    df.sort_values(["Century","Name"], inplace=True)
    df["Party"]=df["pp"].replace(party_dict)

    # Changing None to ''
    mask = df.applymap(lambda x: x is None)
    cols = df.columns[(mask).any()]
    for col in df[cols]:
        df.loc[mask[col], col] = ''
    
    # Transformed dataset
    trans_df = df[["Name", "Party", "From", "president"]]
    
    trans_df.columns = ["Name", "Party", "Presidential term", "President number"]
    trans_df['Ingestion Time'] = datetime.now()
    
    # To JSON
    trans_json = trans_df.to_json(orient = "records")
    return trans_json


if __name__ == "__main__":
    app.run(debug=True, port=5002)