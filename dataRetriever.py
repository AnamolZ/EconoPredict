import requests
import pandas as pd
from bs4 import BeautifulSoup

url = ""
r = requests.get(url)
print(r)