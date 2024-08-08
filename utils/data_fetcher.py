import logging

import alpaca_trade_api as tradeapi
from config.credentials import API_KEY, API_SECRET, BASE_URL
from utils.logger import log_message

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def get_historical_data(symbol, timeframe, limit):
    try:
        barset = api.get_barset(symbol, timeframe, limit=limit)
        log_message(f"Fetched historical data for {symbol}")
        return barset[symbol]
    except Exception as e:
        log_message(f"Error fetching historical data for {symbol}: {str(e)}", level=logging.ERROR)
        return []

# Example usage:
# data = get_historical_data('AAPL', 'day', 100)
# for bar in data:
#     print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)
