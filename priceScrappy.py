from bs4 import BeautifulSoup
import requests
import yfinance as yf
from datetime import datetime, timedelta
import os
import pandas as pd

class StockPrice:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.url = f'https://finance.yahoo.com/quote/{stock_symbol}/'
        self.soup = None
        self.training_data_path = 'TrainingData.csv'
        self.monthly_data_path = 'MonthlyData.csv'

    def scrape_price(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
            price_tag = self.soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            price = price_tag.text if price_tag else 'N/A'
            return float(price)
        except requests.exceptions.RequestException as e:
            print(f'Error fetching data: {e}')
            return None

    def history_training_data(self):
        try:
            today = datetime.utcnow()
            three_months_ago = today - timedelta(days=90)
            training_data = yf.download(self.stock_symbol, start=three_months_ago, end=today, interval='1d')
            training_data.to_csv(self.training_data_path)
        except Exception as e:
            print(f'Error fetching or saving data: {e}')

    def process_data(self):
        try:
            if not os.path.isfile(self.training_data_path):
                print(f'{self.training_data_path} does not exist.')
                self.history_training_data()
            else:
                self.history_training_data()

            stock_data = pd.read_csv(self.training_data_path)
            stock_data['Date'] = pd.to_datetime(stock_data['Date'])
            stock_data.set_index('Date', inplace=True)

            stock_data['Volume'] = stock_data['Volume'].astype(str).str.replace(",", "", regex=False)
            stock_data['Volume'] = pd.to_numeric(stock_data['Volume'], errors='coerce').astype('Int64')

            stock_data = stock_data.apply(pd.to_numeric, errors='coerce').sort_index()

            stock_data.reset_index().to_csv(self.training_data_path, index=False)

            one_month_ago = datetime.now() - timedelta(days=30)
            recent_data = stock_data.loc[one_month_ago:].reset_index()
            recent_data.to_csv(self.monthly_data_path, index=False)

        except Exception as e:
            print(f'Error processing stock data: {e}')

# For Manual Testing
if __name__ == "__main__":
    stock_price = StockPrice("AMZN")
    print(stock_price.scrape_price())
    stock_price.history_training_data()
    stock_price.process_data()