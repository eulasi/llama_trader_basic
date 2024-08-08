import logging

import alpaca_trade_api as tradeapi
from config.credentials import API_KEY, API_SECRET, BASE_URL
from utils.logger import log_message
from config.symbols import symbol_list

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def get_historical_data(symbol, timeframe, limit):
    try:
        barset = api.get_barset(symbol, timeframe, limit=limit)
        log_message(f"Fetched historical data for {symbol}")
        return barset[symbol]
    except Exception as e:
        log_message(f"Error fetching historical data for {symbol}: {str(e)}", level=logging.ERROR)
        return []

def fetch_data_for_all_symbols(timeframe, limit):
    all_data = {}
    for symbol in symbol_list:
        all_data[symbol] = get_historical_data(symbol, timeframe, limit)
    return all_data
