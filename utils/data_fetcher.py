import logging
import alpaca_trade_api as tradeapi
from config.credentials import API_KEY, API_SECRET, BASE_URL
from utils.logger import log_message
from config.symbols import symbol_list

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def get_historical_data(symbol, timeframe, start=None, end=None):
    try:
        # Handle different timeframes according to API requirements
        if timeframe == '1Day':
            tf = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Day)
        elif timeframe == '1Hour':
            tf = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Hour)
        elif timeframe == '1Min':
            tf = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Minute)
        elif timeframe == '1Week':
            tf = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Week)
        elif timeframe == '1Month':
            tf = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Month)
        else:
            # Handle custom minute intervals (e.g., '15Min')
            if 'Min' in timeframe:
                minutes = int(timeframe.replace('Min', ''))
                tf = tradeapi.TimeFrame(minutes, tradeapi.TimeFrameUnit.Minute)
            else:
                raise ValueError(f"Invalid timeframe: {timeframe}")

        if start and end:
            barset = api.get_bars(symbol, tf, start=start, end=end)
        else:
            barset = api.get_bars(symbol, tf, limit=1)  # Fetch the latest bar for live data

        log_message(
            f"Fetched historical data for {symbol} from {start} to {end}" if start and end else f"Fetched latest "
                                                                                                f"historical data for "
                                                                                                f"{symbol}")
        return barset
    except Exception as e:
        log_message(f"Error fetching historical data for {symbol}: {str(e)}", level=logging.ERROR)
        return []


def fetch_data_for_all_symbols(timeframe, start=None, end=None):
    all_data = {}
    for symbol in symbol_list:
        if start and end:
            all_data[symbol] = get_historical_data(symbol, timeframe, start, end)
        else:
            all_data[symbol] = get_historical_data(symbol, timeframe)
    return all_data
