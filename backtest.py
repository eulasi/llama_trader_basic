import numpy as np
import pandas as pd
from utils.data_fetcher import get_historical_data
from strategies.moving_average_crossover import moving_average_crossover


def backtest(strategy, symbol, start_date, end_date):
    data = get_historical_data(symbol, 'day', start_date, end_date)
    closing_prices = [bar.c for bar in data]

    signals = strategy(closing_prices)

    # Assume starting with $1000
    initial_cash = 1000
    shares = 0
    cash = initial_cash

    for signal in signals:
        if signal == 'buy':
            shares += 1
            cash -= closing_prices.pop(0)
        elif signal == 'sell':
            cash += closing_prices.pop(0)
            shares -= 1

    # Final portfolio value
    portfolio_value = cash + shares * closing_prices[-1]
    return portfolio_value


def main():
    symbol = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    strategy = moving_average_crossover

    final_portfolio_value = backtest(strategy, symbol, start_date, end_date)
    print(f"Final portfolio value: ${final_portfolio_value}")


if __name__ == "__main__":
    main()
