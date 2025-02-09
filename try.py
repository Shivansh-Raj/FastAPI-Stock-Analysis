# 7XZM50MIDWIR5EDB

import requests

API_KEY = '7XZM50MIDWIR5EDB'
symbol = 'AAPL'
interval = '60min'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}&adjusted=false'

response = requests.get(url)
data = response.json()

# Print the latest 5-minute data
print(data[f'Time Series ({interval})'].get('2025-02-07 19:00:00'))
