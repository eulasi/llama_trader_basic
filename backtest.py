from utils.data_fetcher import get_historical_data
from strategies.moving_average_crossover import moving_average_crossover
from utils.logger import log_message


def backtest(strategy, symbol, start_date, end_date):
    data = get_historical_data(symbol, 'day', start_date, end_date)
    if not data:
        log_message(f"No data fetched for {symbol} from {start_date} to {end_date}")
        return 0

    closing_prices = [bar.c for bar in data]

    # Assuming strategy returns signals based on closing prices
    signals = strategy(closing_prices)

    # Assume starting with $250
    initial_cash = 250
    shares = 0
    cash = initial_cash

    for signal, price in zip(signals, closing_prices):
        if signal == 'buy':
            shares += 1
            cash -= price
        elif signal == 'sell':
            cash += price
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
