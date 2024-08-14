import logging
import time
import alpaca_trade_api as tradeapi
from config.credentials import API_KEY, API_SECRET, BASE_URL
from utils.logger import log_message
from config.symbols import symbol_list
from utils.data_fetcher import get_historical_data  # Ensure this import is added

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Cache to store recent data
data_cache = {}


def convert_timeframe(timeframe):
    """Convert a string-based timeframe to an Alpaca TimeFrame object."""
    if timeframe == '1Day':
        return tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Day)
    elif timeframe == '1Hour':
        return tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Hour)
    elif timeframe == '1Min':
        return tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Minute)
    elif timeframe == '1Week':
        return tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Week)
    elif timeframe == '1Month':
        return tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Month)
    elif 'Min' in timeframe:
        minutes = int(timeframe.replace('Min', ''))
        return tradeapi.TimeFrame(minutes, tradeapi.TimeFrameUnit.Minute)
    else:
        raise ValueError(f"Invalid timeframe: {timeframe}")


def get_live_data(symbol, timeframe, cache_duration=60):
    try:
        current_time = time.time()
        # Check if the data is already cached and is still valid
        if symbol in data_cache and (current_time - data_cache[symbol]['timestamp']) < cache_duration:
            log_message(f"Using cached data for {symbol}")
            return data_cache[symbol]['data']

        # Convert timeframe if it's a string
        if isinstance(timeframe, str):
            timeframe = convert_timeframe(timeframe)

        # Fetch the latest live bar
        barset = api.get_bars(symbol, timeframe, limit=1)
        log_message(f"Fetched latest live data for {symbol}: {barset}")

        # Cache the data
        data_cache[symbol] = {
            'data': barset,
            'timestamp': current_time
        }
        return barset
    except Exception as e:
        log_message(f"Error fetching live data for {symbol}: {str(e)}", level=logging.ERROR)
        return []


def fetch_supplemented_data(symbol, timeframe, required_bars=30):
    # Fetch a larger set of historical data
    historical_data = get_historical_data(symbol, timeframe)
    # Slice the data to get the required number of bars
    historical_data = historical_data[-(required_bars - 1):]
    live_data = get_live_data(symbol, timeframe, cache_duration=60)
    return historical_data + live_data


def fetch_live_data_for_all_symbols(timeframe):
    all_data = {}
    for symbol in symbol_list:
        try:
            data = fetch_supplemented_data(symbol, timeframe)  # Use supplemented data
            if not data:
                log_message(f"{symbol}: No live data fetched. Check symbol validity and timeframe.",
                            level=logging.WARNING)
            all_data[symbol] = data
        except Exception as e:
            log_message(f"Error fetching live data for {symbol}: {str(e)}", level=logging.ERROR)
            all_data[symbol] = None
    return all_data
