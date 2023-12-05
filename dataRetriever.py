import requests

r = requests.get("https://www.nasdaq.com/market-activity/stocks/aapl/historical")
print(r)