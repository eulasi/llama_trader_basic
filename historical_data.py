import os
import pandas as pd
from utils.data_fetcher import fetch_data_for_all_symbols
import alpaca_trade_api as tradeapi


def save_historical_data(symbol, data, timeframe):
    directory = 'data/historical_data'
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
    df.to_csv(filename, index=False)
    print(f"Saved historical data for {symbol} to {filename}")


def main():
    # Set the timeframe using the appropriate TimeFrame and TimeFrameUnit
    timeframe = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Day)
    all_data = fetch_data_for_all_symbols(timeframe)

    for symbol, data in all_data.items():
        if not data:
            continue
        save_historical_data(symbol, data, '1Day')  # Using '1Day' to match the correct timeframe


if __name__ == "__main__":
    main()
