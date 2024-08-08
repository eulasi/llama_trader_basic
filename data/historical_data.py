import pandas as pd
from utils.data_fetcher import fetch_data_for_all_symbols

def save_historical_data(symbol, data, timeframe):
    filename = f"data/historical_data/{symbol}_{timeframe}.csv"
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
    timeframe = 'day'
    limit = 100
    all_data = fetch_data_for_all_symbols(timeframe, limit)

    for symbol, data in all_data.items():
        if not data:
            continue
        save_historical_data(symbol, data, timeframe)

if __name__ == "__main__":
    main()
