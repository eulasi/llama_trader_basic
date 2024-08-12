import logging
import alpaca_trade_api as tradeapi
from config.credentials import API_KEY, API_SECRET, BASE_URL
from utils.logger import log_message
from config.symbols import symbol_list

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


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


def get_live_data(symbol, timeframe):
    try:
        # Convert timeframe if it's a string
        if isinstance(timeframe, str):
            timeframe = convert_timeframe(timeframe)

        # Fetch the latest live bar
        barset = api.get_bars(symbol, timeframe, limit=1)
        log_message(f"Fetched latest live data for {symbol}: {barset}")
        return barset
    except Exception as e:
        log_message(f"Error fetching live data for {symbol}: {str(e)}", level=logging.ERROR)
        return []


def fetch_live_data_for_all_symbols(timeframe):
    all_data = {}
    for symbol in symbol_list:
        try:
            data = get_live_data(symbol, timeframe)
            if not data:
                log_message(f"{symbol}: No live data fetched. Check symbol validity and timeframe.", level=logging.WARNING)
            all_data[symbol] = data
        except Exception as e:
            log_message(f"Error fetching live data for {symbol}: {str(e)}", level=logging.ERROR)
            all_data[symbol] = None
    return all_data
