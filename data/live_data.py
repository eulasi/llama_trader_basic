import time
import pandas as pd
from utils.data_fetcher import get_historical_data


def save_live_data(symbol, timeframe, interval, filename):
    while True:
        data = get_historical_data(symbol, timeframe, limit=1)
        latest_bar = data[-1]

        df = pd.DataFrame([{
            'time': latest_bar.t,
            'open': latest_bar.o,
            'high': latest_bar.h,
            'low': latest_bar.l,
            'close': latest_bar.c,
            'volume': latest_bar.v
        }])

        df.to_csv(filename, mode='a', header=False, index=False)
        print(f"Appended live data for {symbol} to {filename}")

        time.sleep(interval)


def main():
    symbol = 'AAPL'
    timeframe = 'minute'
    interval = 60  # Fetch data every 60 seconds
    filename = f"data/live_data/{symbol}_{timeframe}.csv"

    save_live_data(symbol, timeframe, interval, filename)


if __name__ == "__main__":
    main()
