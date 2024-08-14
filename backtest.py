from config.symbols import symbol_list
from strategies.moving_average_crossover import moving_average_crossover
from utils.data_fetcher import fetch_data_for_all_symbols, convert_timeframe
from utils.logger import log_message


def generate_signals(orders):
    """ Convert detailed order objects into simple 'buy', 'sell', or 'hold' signals. """
    signals = []
    for order in orders:
        if order['side'] == 'buy':
            signals.append('buy')
        elif order['side'] == 'sell':
            signals.append('sell')
        else:
            signals.append('hold')
    return signals


def backtest(strategy, symbol, start_date, end_date):
    # Convert 'day' string to TimeFrame object
    timeframe = convert_timeframe('1Day')
    data = fetch_data_for_all_symbols(timeframe, start=start_date, end=end_date).get(symbol)
    if not data:
        log_message(f"No data fetched for {symbol} from {start_date} to {end_date}")
        return 0

    # Pass the fetched data directly to the strategy
    orders = strategy(data)  # Pass data directly here

    # Convert the detailed orders into simple signals
    signals = generate_signals(orders)

    initial_cash = 250
    shares = 0
    cash = initial_cash

    closing_prices = [bar._raw['c'] for bar in data]  # Access the closing price through _raw

    for signal, price in zip(signals, closing_prices):
        if signal == 'buy' and cash >= price:
            shares += 1
            cash -= price
        elif signal == 'sell' and shares > 0:
            cash += price
            shares -= 1

    portfolio_value = cash + shares * closing_prices[-1]
    log_message(f"Backtest completed for {symbol}. Final portfolio value: ${portfolio_value}")
    return portfolio_value


def main():
    start_date = '2023-01-01'
    end_date = '2023-12-31'

    # Define your short and long window lengths
    short_window = 3
    long_window = 7

    # Strategy function that takes the pre-fetched data as input
    def strategy(data):
        risk_manager = None  # Define your RiskManager here if needed
        return moving_average_crossover(risk_manager, data, short_window=short_window, long_window=long_window)

    for symbol in symbol_list:
        final_portfolio_value = backtest(strategy, symbol, start_date, end_date)
        print(f"Final portfolio value for {symbol}: ${final_portfolio_value:.2f}")


if __name__ == "__main__":
    main()
