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


def get_live_data(symbol, use_latest_methods=True):
    try:
        current_time = time.time()

        # Use the direct methods to get the latest bar, trade, and quote
        if use_latest_methods:
            bar = api.get_latest_bar(symbol)
            trade = api.get_latest_trade(symbol)
            quote = api.get_latest_quote(symbol)

            log_message(f"Fetched latest bar for {symbol}: {bar}")
            log_message(f"Fetched latest trade for {symbol}: {trade}")
            log_message(f"Fetched latest quote for {symbol}: {quote}")

            # Cache the data
            data_cache[symbol] = {
                'data': [bar],  # Store the bar data as a list to keep the format consistent
                'timestamp': current_time
            }
            return [bar]  # Return the latest bar as a list

        else:
            # Use TimeFrame(1, TimeFrameUnit.Minute) to specify a 1-minute timeframe
            timeframe = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Minute)
            barset = api.get_bars(symbol, timeframe, limit=1)
            log_message(f"Fetched latest live data for {symbol}: {barset}")
            last_bar = barset[-1] if barset else None
            if last_bar:
                last_bar_time = last_bar.t.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
                log_message(f"Last bar for {symbol} fetched at {last_bar_time} with close price {last_bar.c}")

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
    live_data = get_live_data(symbol)
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
