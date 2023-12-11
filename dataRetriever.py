import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import os
import pandas as pd
from datetime import datetime, timedelta

# symbols = ['AMZN', 'GOOGL', 'TSLA', 'NFLX', 'META', 'AMZN', 'AMD', 'UBER']

def func(req):
    current_datetime = datetime.now()
    TrainningData = "TrainningData.csv" 
    MonthlyData = "MonthlyData.csv"
    os.remove(MonthlyData) if os.path.exists(MonthlyData) else None
    os.remove(TrainningData) if os.path.exists(TrainningData) else None
    
    url = f"https://finance.yahoo.com/quote/{req}/history?p={req}"

    column_headers = []

    headers = {"User-Agent": UserAgent().random}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    table_tag = soup.find("table", class_="W(100%) M(0)")
    headers_tag = table_tag.find_all("th")

    for header_tag in headers_tag:
        column_headers.append(header_tag.text)

    df = pd.DataFrame(columns=column_headers)
    data_rows = table_tag.find_all("tr")[1:101]

    for row_tag in data_rows:
        data_cells = row_tag.find_all("td")
        row_data = [cell.text for cell in data_cells]
        df_length = len(df)
        df.loc[df_length] = row_data

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df["Volume"] = pd.to_numeric(df["Volume"].str.replace(",", ""), errors="coerce").astype('Int64')

    df[column_headers[1:]] = df[column_headers[1:]].apply(pd.to_numeric, errors='coerce')
    df.sort_index(inplace=True)

    df_rdc = df.reset_index()
    df_rdc.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    df_rdc.to_csv('TrainningData.csv', index=False)

    file_path = "TrainningData.csv"
    df = pd.read_csv(file_path)

    one_month_ago = current_datetime - timedelta(days=41)
    formatted_current_date = current_datetime.strftime("%Y-%m-%d")
    formatted_one_month_ago = one_month_ago.strftime("%Y-%m-%d")

    df["Date"] = pd.to_datetime(df["Date"])
    filtered_dates = df[(df["Date"] >= formatted_one_month_ago) & (df["Date"] <= formatted_current_date)]
    date = {"Date": filtered_dates["Date"].dt.strftime('%Y-%m-%d').tolist()}

    filtered_dates.to_csv('MonthlyData.csv', index=False)
    return df_rdc["Close"][len(df_rdc)-1]