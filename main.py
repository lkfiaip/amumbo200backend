from flask import Flask, jsonify
import requests
import pandas as pd
import datetime

app = Flask(__name__)

# Replace with your API endpoint and API key
API_URL = "https://www.alphavantage.co/query"
API_KEY = "ZM89TJECHAKFW46A"

def get_nasdaq_data():
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": "^IXIC",  # NASDAQ index symbol for Alpha Vantage
        "apikey": API_KEY,
        "outputsize": "full"
    }
    response = requests.get(API_URL, params=params)
    data = response.json()["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(data, orient="index", dtype=float)
    df.index = pd.to_datetime(df.index)
    return df

def calculate_sma200(df):
    df['SMA200'] = df['4. close'].rolling(window=200).mean()
    latest_sma200 = df['SMA200'].iloc[-1]
    return latest_sma200

@app.route('/sma200', methods=['GET'])
def sma200():
    data = get_nasdaq_data()
    sma200 = calculate_sma200(data)
    return jsonify({"sma200": sma200})

if __name__ == '__main__':
    app.run(debug=True)

