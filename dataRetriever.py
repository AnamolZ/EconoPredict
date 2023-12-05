import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.nasdaq.com/market-activity/stocks/aapl/historical"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
