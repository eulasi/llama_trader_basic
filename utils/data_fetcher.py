import logging
import alpaca_trade_api as tradeapi
from config.credentials import API_KEY, API_SECRET, BASE_URL
from utils.logger import log_message
from config.symbols import symbol_list

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def convert_timeframe(timeframe):
    """Convert a string-based timeframe to an Alpaca TimeFrame object."""
    timeframe_mapping = {
        '1Day': tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Day),
        '1Hour': tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Hour),
        '1Min': tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Minute),
        '1Week': tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Week),
        '1Month': tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Month)
    }

    # Handle custom minute-based timeframes
    if 'Min' in timeframe:
        minutes = int(timeframe.replace('Min', ''))
        return tradeapi.TimeFrame(minutes, tradeapi.TimeFrameUnit.Minute)

    return timeframe_mapping.get(timeframe, ValueError(f"Invalid timeframe: {timeframe}"))


def get_historical_data(symbol, timeframe, start=None, end=None):
    try:
        # Convert timeframe if it's a string
        timeframe = convert_timeframe(timeframe) if isinstance(timeframe, str) else timeframe

        all_bars = []
        while True:
            barset = api.get_bars(symbol, timeframe, start=start, end=end)
            if not barset:
                break
            all_bars.extend(barset)

            # If less than 1000 bars are returned, it's likely the end of the data
            if len(barset) < 1000:
                break

            # Update the start date for the next batch
            start = barset[-1].t.strftime('%Y-%m-%d')

        log_message(f"Fetched {len(all_bars)} historical data points for {symbol} from {start} to {end}")
        return all_bars

    except Exception as e:
        log_message(f"Error fetching historical data for {symbol}: {str(e)}", level=logging.ERROR)
        return []


def fetch_data_for_all_symbols(timeframe, start=None, end=None):
    all_data = {}
    for symbol in symbol_list:
        try:
            data = get_historical_data(symbol, timeframe, start, end)
            if not data:
                log_message(f"{symbol}: No data fetched. Check symbol validity, timeframe, and data availability.",
                            level=logging.WARNING)
            all_data[symbol] = data
        except Exception as e:
            log_message(f"Error fetching data for {symbol}: {str(e)}", level=logging.ERROR)
            all_data[symbol] = None
    return all_data
