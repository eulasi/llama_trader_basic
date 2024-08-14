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


def main(timeframe='1Day'):
    # Convert string-based timeframe to Alpaca TimeFrame object
    alpaca_timeframe = tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Day)  # Adjust as needed

    all_data = fetch_data_for_all_symbols(alpaca_timeframe)

    for symbol, data in all_data.items():
        if not data:
            continue
        save_historical_data(symbol, data, timeframe)


if __name__ == "__main__":
    # Pass a different timeframe as an argument if needed, e.g., '1Hour', '1Min'
    main(timeframe='1Day')
