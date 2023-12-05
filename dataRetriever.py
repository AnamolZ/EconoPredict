import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

url = "https://finance.yahoo.com/quote/TSLA/history?p=TSLA"

column_headers = []

headers = {"User-Agent": UserAgent().random}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

table_tag = soup.find("table", class_="W(100%) M(0)")
headers_tag = table_tag.find_all("th")

for header_tag in headers_tag:
    column_headers.append(header_tag.text)

df = pd.DataFrame(columns=column_headers)
data_rows = table_tag.find_all("tr")[1:11]

for row_tag in data_rows:
    data_cells = row_tag.find_all("td")
    row_data = [cell.text for cell in data_cells]
    df_length = len(df)
    df.loc[df_length] = row_data

print(type(df))
