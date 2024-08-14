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
    timeframe = convert_timeframe('1Day')
    data = fetch_data_for_all_symbols(timeframe, start=start_date, end=end_date).get(symbol)
    if not data:
        log_message(f"No data fetched for {symbol} from {start_date} to {end_date}")
        return 0

    orders = strategy(data, symbol)  # Pass data and symbol directly

    signals = generate_signals(orders)

    initial_cash = 250
    shares = 0
    cash = initial_cash

    for signal, price in zip(signals, [bar._raw['c'] for bar in data]):
        if signal == 'buy' and cash >= price:
            shares += 1
            cash -= price
        elif signal == 'sell' and shares > 0:
            cash += price
            shares -= 1

    portfolio_value = cash + shares * data[-1]._raw['c']
    log_message(f"Backtest completed for {symbol}. Final portfolio value: ${portfolio_value}")
    return portfolio_value


def main():
    start_date = '2023-01-01'
    end_date = '2023-12-31'

    short_window = 3
    long_window = 7

    def strategy(data, current_symbol):
        risk_manager = None  # Define your RiskManager here if needed
        return moving_average_crossover(risk_manager, data, current_symbol, short_window=short_window,
                                        long_window=long_window)

    for symbol in symbol_list:
        final_portfolio_value = backtest(strategy, symbol, start_date, end_date)
        print(f"Final portfolio value for {symbol}: ${final_portfolio_value:.2f}")


if __name__ == "__main__":
    main()
