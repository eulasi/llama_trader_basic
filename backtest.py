from utils.data_fetcher import fetch_data_for_all_symbols
from strategies.moving_average_crossover import moving_average_crossover
from utils.logger import log_message
from config.symbols import symbol_list


def backtest(strategy, symbol, start_date, end_date):
    data = fetch_data_for_all_symbols('day', start=start_date, end=end_date).get(symbol)
    if not data:
        log_message(f"No data fetched for {symbol} from {start_date} to {end_date}")
        return 0

    closing_prices = [bar.close for bar in data]

    signals = strategy(closing_prices)

    initial_cash = 1000
    shares = 0
    cash = initial_cash

    for signal, price in zip(signals, closing_prices):
        if signal == 'buy':
            shares += 1
            cash -= price
        elif signal == 'sell':
            cash += price
            shares -= 1

    portfolio_value = cash + shares * closing_prices[-1]
    return portfolio_value


def main():
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    strategy = moving_average_crossover

    for symbol in symbol_list:
        final_portfolio_value = backtest(strategy, symbol, start_date, end_date)
        print(f"Final portfolio value for {symbol}: ${final_portfolio_value}")


if __name__ == "__main__":
    main()
