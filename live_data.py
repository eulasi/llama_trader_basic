import logging
import os
import time
import pandas as pd
from utils.data_fetcher import get_historical_data
from utils.logger import log_message
from config.symbols import symbol_list
import alpaca_trade_api as tradeapi


def save_live_data(symbol, data, timeframe):
    directory = 'data/live_data'
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/{symbol}_{timeframe}.csv"
    df = pd.DataFrame([{
        'time': bar.t,
        'open': bar.o,
        'high': bar.h,
        'low': bar.l,
        'close': bar.c,
        'volume': bar.v
    } for bar in data])
    df.to_csv(filename, mode='a', header=False, index=False)
    print(f"Appended live data for {symbol} to {filename}")


def fetch_and_save_live_data(timeframe='1Min'):
    log_message("Starting live data fetching process")
    alpaca_timeframe = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Minute)  # Default to 1-minute bars

    while True:
        for symbol in symbol_list:
            data = get_historical_data(symbol, alpaca_timeframe)
            if not data:
                log_message(f"No live data fetched for {symbol}")
                continue
            save_live_data(symbol, data, timeframe)
            log_message(f"Appended live data for {symbol}")

        # Sleep for 60 seconds before fetching the next batch of live data
        time.sleep(60)


def main():
    try:
        fetch_and_save_live_data(timeframe='1Min')
    except Exception as e:
        log_message(f"Error in live data fetching: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
