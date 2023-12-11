#Third party imports
import json
import re
import asyncio
import httpx
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

#FastAPI imports
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional

#Imports From PulseAI
from PulseAI import PulseAI

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'GOOG', 'NVDA', 'BA', 'NFLX']

def requirement(request: Request, Stock: Optional[str] = None):
    return Stock

async def fetch_data(client, semaphore, stock, data):

    async with semaphore:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        url = f'https://www.google.com/finance/quote/{stock}:NASDAQ'

        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            targetDiv = soup.find('div', class_='YMlKec fxKbKc')

            if targetDiv:
                stockPrice = float(targetDiv.text.strip()[1:])
                pageTitle = soup.title.text
                stockName = pageTitle.split('Stock')[0].strip()
                stockSymbolShort = re.search(r'\((.*?)\)', stockName).group(1)
                data[stockSymbolShort] = stockPrice
            return data
        else:
            print(f'Failed to retrieve the page for {stock}. Status code: {response.status_code}')

async def fetch_all_stocks(stock_symbols):
    data = {}
    semaphore = asyncio.Semaphore(8)
    async with httpx.AsyncClient() as client:
        tasks = [fetch_data(client, semaphore, stock, data.copy()) for stock in stock_symbols]
        results = await asyncio.gather(*tasks)
    findata = {}
    for result in results:
        findata.update(result)
    return findata

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, Stock: str = Depends(requirement)):
    prediction = "Hi! From Anamol"
    symbols = ['AMZN', 'GOOGL', 'TSLA', 'NFLX', 'META', 'AMZN', 'AMD', 'UBER']
    if Stock in symbols:
        prediction = ''
        prediction = PulseAI(Stock)
    return templates.TemplateResponse("index.html", {"request": request, "Prediction": prediction})

@app.get("/favicon.ico")
async def favicon(request: Request):
    return "No Favicon"

@app.get("/stock_data_generator")
async def stock_data_generator(request: Request):
    async def generate():
        while True:
            result_var = await fetch_all_stocks(symbols)
            stock_prices = json.dumps(result_var)
            yield f"data: {stock_prices}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/weekData")
async def readfile(request: Request):
    file_path = 'MonthlyData.csv'
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return {"error": "File not found"}
    data_dict = {column: df[column].tolist() for column in df.columns}
    return data_dict