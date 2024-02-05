#Third party imports
import json
import re
import asyncio
import httpx
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import base64
import psycopg2
import random
import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#FastAPI imports
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional

#Imports From PulseAI
from PulseAI import PulseAI

#Imports From Func
from dataRetriever import func

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(host="localhost", dbname="postgres", 
                        user="postgres", password="1379", port="5432")

symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'GOOG', 'NVDA', 'BA', 'NFLX']

DATABASE_CONFIG = {
    "host": "localhost",
    "dbname": "postgres",
    "user": "postgres",
    "password": "1379",
    "port": "5432",
}

def create_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

def get_data():
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            data = cur.fetchall()
    return data

def requirement(request: Request, Stock: Optional[str] = None):
    return Stock

def send_email(recipient_email, message_body):
    sender_email = 'danamol22@tbc.edu.np'
    sender_password = 'wkwn ongs viit rchu'
    subject = 'Verification Code'
    message = MIMEMultipart()
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(message_body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

def generate_token(seed):
    return random.randint(1, 1000000)

token = None
start_time = None

def validate_token(entered_token):
    global token
    global start_time
    if int(entered_token) == token and (time.time() - start_time) <= 60:
        return "Valid"
    elif (time.time() - start_time) > 60:
        return "Expired"
    else:
        return "Invalid"

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
async def read_root(request: Request):
    prediction = f"Hi! From Dev"
    return templates.TemplateResponse("index.html", {"request": request, "Prediction": prediction})

@app.post("/prediction")
async def prediction(request: Request):
        try:
            stock = (await request.json()).get("stock")
            prediction = PulseAI(stock)
            return prediction
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

global access
access = False

@app.post("/adccess")
async def admin_access(request: Request):
    global access
    try:
        temp = (await request.json()).get("temp")
        if temp == "Admin":
            access = True
        else:
            raise HTTPException(status_code=401, detail="Access Denied")
    except:
        raise HTTPException(status_code=401, detail="Access Denied")

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    global access
    try:
        data = get_data()
        if access:
            return templates.TemplateResponse("admin.html", {"request": request, "data": data})
        else:
            raise HTTPException(status_code=401, detail="Access Denied")
    except:
        raise HTTPException(status_code=401, detail="Access Denied")

@app.post("/verification")
async def verification(request: Request):
    try:
        data = await request.json()
        entered_token = data.get('vcode')
        cache_email = data.get('cacheemail')
        if (validate_token(entered_token) == "Valid"):
            verification_status(f'{cache_email}', 'verified')
            return "Valid"
        else:
            return "Invalid"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logout")
async def logout(request: Request):
    try:
        global access
        data = await request.json()
        access = data.get("access", False)
        print(access)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/favicon.ico")
async def favicon(request: Request):
    return "No Favicon"

@app.post("/add")
async def add(request: Request):
    try:
        data = await request.json()
        with create_connection() as conn:
            with conn.cursor() as cur:
                sql_query = "INSERT INTO users (email, password, admin, verified) VALUES (%s, %s, %s, %s)"
                try:
                    encrypted_password = base64.b64encode(data['password'].encode('utf-8')).decode('utf-8')
                    cur.execute(sql_query, (data['email'], encrypted_password, data['admin'], data['verified']))
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"Error adding user: {e}")

        return {"User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update")
async def update_user(request: Request):
    try:
        data = await request.json()
        email = data.get('email')
        if email:
            encrypted_password = base64.b64encode(data['password'].encode('utf-8')).decode('utf-8')
            
            with create_connection() as conn:
                with conn.cursor() as cur:
                    sql_query = "UPDATE users SET password = %s, admin = %s, verified = %s WHERE email = %s"
                    try:
                        cur.execute(sql_query, (encrypted_password, data['admin'], data['verified'], email))
                        conn.commit()
                        return {"updated successfully"}
                    except Exception as e:
                        conn.rollback()
                        raise HTTPException(status_code=500, detail=f"Error updating data: {e}")
        else:
            raise HTTPException(status_code=400, detail="Email is required in the request data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_data(email):
    with create_connection() as conn:
        with conn.cursor() as cur:
            sql_query = "DELETE FROM users WHERE email = %s"
            try:
                cur.execute(sql_query, (email,))
                conn.commit()
                print("Delete successful")
            except Exception as e:
                conn.rollback()
                print(f"Error deleting data: {e}")

@app.post("/delete")
async def delete(request: Request):
    try:
        data = await request.json()
        email = data.get('email')
        if email:
            delete_data(email)
            return {"message": f"Data for email {email} deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Email is required in the request data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    try:
        file_path = 'MonthlyData.csv'
        df = pd.read_csv(file_path)
        data_dict = {column: df[column].tolist() for column in df.columns}
        return data_dict
    except FileNotFoundError:
        return "File not found"

@app.post("/stockhistory")
async def read_root(request: Request):
    try:
        data = await request.json()
        stock = data.get("stock")
        if stock is not None:
            func(stock)
            return "Processing request successfully"
        else:
            raise HTTPException(status_code=400, detail="Invalid request data")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logging")
async def logging(request: Request):
    conn = create_connection()
    cur = None
    try:
        cur = conn.cursor()
        data = await request.json()
        email_value = data.get('email')
        encrypted_password = base64.b64encode(data.get('password').encode('utf-8')).decode('utf-8')
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email_value, encrypted_password))
        user_data = cur.fetchone()
        if user_data:
            _, _, admin_status, verified_status = user_data
            if admin_status:
                return "Admin"
            elif verified_status == 'Verified':
                return "Valid"
            else:
                return "Unverified"
        else:
            return "Invalid"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        conn.close()

@app.post("/signingup")
async def signingup(request: Request):
    global token
    global start_time
    
    conn = create_connection()
    cur = None
    
    seed_value = random.randint(1, 102042424)
    token = generate_token(seed_value)
    start_time = time.time()
    
    try:
        cur = conn.cursor()
        data = await request.json()
        email_value = data.get('email1')
        encrypted_password = base64.b64encode(data.get('password1').encode('utf-8')).decode('utf-8')
        admin_status = data.get('admin', False)
        verified_status = data.get('verified', 'notverified')

        cur.execute("INSERT INTO users (email, password, admin, verified) VALUES (%s, %s, %s, %s)",
                    (email_value, encrypted_password, admin_status, verified_status))

        conn.commit()
        recipient_email = 'anmoldkl971@gmail.com'
        message_body = f'Verification Code {token}.'
        send_email(recipient_email, message_body)
        return f"Signed up In {email_value}, {encrypted_password}, Admin: {admin_status}, Verified: {verified_status}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        conn.close()

def verification_status(email, new_status):
    conn = psycopg2.connect(host="localhost", dbname="postgres", 
                        user="postgres", password="1379", port="5432")
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET verified = %s
        WHERE email = %s
    """, (new_status, email))

    conn.commit()
    cur.close()
    conn.close()

@app.post("/verification")
async def verification(request: Request):
    try:
        data = await request.json()
        entered_token = data.get('vcode')
        cache_email = data.get('cacheemail')
        if (validate_token(entered_token) == "Valid"):
            verification_status(f'{cache_email}', 'verified')
            return "Valid"
        else:
            return "Invalid"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))