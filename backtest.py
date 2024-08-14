from config.symbols import symbol_list
from strategies.moving_average_crossover import moving_average_crossover
from utils.data_fetcher import fetch_data_for_all_symbols, convert_timeframe
from utils.logger import log_message
from utils.risk_management import RiskManager


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


def backtest(strategy, symbol, symbol_data, initial_cash):
    if not symbol_data:
        log_message(f"No data available for {symbol}")
        return 0

    # Instantiate the RiskManager with the desired parameters
    risk_manager = RiskManager(
        max_loss_per_trade=50,  # Example value, adjust as needed
        max_daily_loss=100,  # Example value, adjust as needed
        initial_capital=initial_cash,  # Should match the initial cash used in the backtest
        risk_percentage=20  # Example: 20% risk per trade
    )

    closing_prices = [bar._raw['c'] for bar in symbol_data]

    # Generate detailed orders from the strategy
    orders = strategy(symbol_data, symbol, risk_manager)

    signals = generate_signals(orders)

    shares = 0
    cash = initial_cash
    trade_count = 0  # Track the number of trades

    for signal, price in zip(signals, closing_prices):
        position_size = risk_manager.calculate_position_size(price)
        if position_size == 0:
            continue  # Skip trade if position size is zero

        if signal == 'buy' and cash >= price * position_size:
            shares += position_size
            cash -= price * position_size
            trade_count += 1
        elif signal == 'sell' and shares >= position_size:
            cash += price * position_size
            shares -= position_size
            trade_count += 1

    final_portfolio_value = cash + shares * closing_prices[-1]

    # Calculate profit/loss
    profit_loss = final_portfolio_value - initial_cash
    log_message(f"Backtest completed for {symbol}. Trades executed: {trade_count}. "
                f"Final portfolio value: ${final_portfolio_value:.2f} (Profit: ${profit_loss:.2f})"
                if profit_loss > 0 else
                f"Final portfolio value: ${final_portfolio_value:.2f} (Loss: ${profit_loss:.2f})")

    return final_portfolio_value


def main():
    # Set Start and End Date
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    # 1Day, 1Hour, 1Min, 1Sec
    timeframe = convert_timeframe('1Day')

    # Fetch data for all symbols upfront
    all_data = fetch_data_for_all_symbols(timeframe, start=start_date, end=end_date)

    # Define your short and long window lengths
    short_window = 3
    long_window = 7

    # Set the initial cash value, dynamically adjustable
    initial_cash = 250

    # Define the strategy function
    def strategy(symbol_data, current_symbol, risk_manager):
        # Use the risk_manager within the strategy if needed
        return moving_average_crossover(risk_manager, symbol_data, current_symbol, short_window=short_window,
                                        long_window=long_window)

    # Run the backtest for each symbol
    for symbol in symbol_list:
        data = all_data.get(symbol)
        final_portfolio_value = backtest(strategy, symbol, data, initial_cash)

        # Calculate profit/loss for terminal output
        profit_loss = final_portfolio_value - initial_cash  # Use dynamic initial_cash value
        if profit_loss > 0:
            print(f"Final portfolio value for {symbol}: ${final_portfolio_value:.2f} (Profit: ${profit_loss:.2f})")
        elif profit_loss < 0:
            print(f"Final portfolio value for {symbol}: ${final_portfolio_value:.2f} (Loss: ${profit_loss:.2f})")
        else:
            print(f"Final portfolio value for {symbol}: ${final_portfolio_value:.2f} (Unchanged)")


if __name__ == "__main__":
    main()
