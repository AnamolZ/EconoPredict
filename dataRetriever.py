import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.nasdaq.com/market-activity/stocks/aapl/historical"
r = requests.get(url)
print(r)