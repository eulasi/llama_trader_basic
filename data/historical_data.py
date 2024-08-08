import pandas as pd
from utils.data_fetcher import get_historical_data


def save_historical_data(symbol, timeframe, limit, filename):
    data = get_historical_data(symbol, timeframe, limit)
    df = pd.DataFrame([{
        'time': bar.t,
        'open': bar.o,
        'high': bar.h,
        'low': bar.l,
        'close': bar.c,
        'volume': bar.v
    } for bar in data])
    df.to_csv(filename, index=False)


def main():
    symbol = 'AAPL'
    timeframe = 'day'
    limit = 100
    filename = f"data/historical_data/{symbol}_{timeframe}.csv"

    save_historical_data(symbol, timeframe, limit, filename)
    print(f"Saved historical data for {symbol} to {filename}")


if __name__ == "__main__":
    main()
