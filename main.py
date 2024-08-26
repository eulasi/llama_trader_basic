import logging
import os
import time
from datetime import datetime
import alpaca_trade_api as tradeapi
import numpy as np
import pandas as pd
from strategies.moving_average_crossover import moving_average_crossover
from utils.live_data_fetcher import fetch_live_data_for_all_symbols
from utils.order_executor import place_order, handle_order_execution
from utils.logger import log_message
from utils.risk_management import RiskManager
from config.credentials import API_KEY, API_SECRET, BASE_URL
from utils.performance_tracker import PerformanceTracker  # Import the PerformanceTracker

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Initialize PerformanceTracker
performance_tracker = PerformanceTracker()


def get_current_positions():
    """Fetch current positions from Alpaca."""
    positions = api.list_positions()
    current_positions = {position.symbol: float(position.qty) for position in positions}
    return current_positions


def get_orders_by_status(status_list):
    """
    Fetch orders from Alpaca filtered by a list of statuses.
    Possible statuses: 'open', 'closed', 'all', 'pending_new', 'accepted', 'partially_filled',
    'filled', 'done_for_day', 'canceled', 'expired', 'replaced', 'pending_cancel',
    'pending_replace', 'stopped', 'rejected', 'suspended', 'calculated'
    """
    orders = api.list_orders(status='all', limit=500)  # Fetch last 500 orders
    filtered_orders = [order for order in orders if order.status in status_list]
    orders_dict = {}
    for order in filtered_orders:
        if order.symbol not in orders_dict:
            orders_dict[order.symbol] = []
        orders_dict[order.symbol].append(order)
    return orders_dict


def modify_or_replace_order(existing_order, new_order_qty, risk_manager):
    """Modify or replace an existing order based on updated strategy conditions."""
    try:
        # Cancel the existing order
        api.cancel_order(existing_order.id)
        log_message(f"Canceled existing order for {existing_order.symbol}: {existing_order.id}", level=logging.INFO)

        # Place a new order with the updated quantity
        new_order = place_order(existing_order.symbol, new_order_qty, existing_order.side, risk_manager=risk_manager)
        log_message(f"Placed new order for {existing_order.symbol}: {new_order.id}", level=logging.INFO)
        return new_order
    except Exception as e:
        log_message(f"Failed to modify or replace order for {existing_order.symbol}: {str(e)}", level=logging.ERROR)
        return None


def pnl_header():
    log_message(f"<Calculated PnL>")


def calculate_pnl(symbol, entry_price, current_price, qty):
    """Calculate profit and loss for a given symbol."""
    pnl = (current_price - entry_price) * qty
    log_message(f"Calculated PnL for {symbol}: ${pnl:.2f}", level=logging.INFO)
    return pnl


def monitor_pnl(current_positions):
    """Monitor and log PnL for current positions."""
    pnl_data = []
    for symbol, qty in current_positions.items():
        entry_price = float(api.get_position(symbol).avg_entry_price)
        current_price = float(api.get_latest_trade(symbol).price)  # Correct method used here
        pnl = calculate_pnl(symbol, entry_price, current_price, qty)
        log_message(f"Current PnL for {symbol}: ${pnl:.2f}", level=logging.INFO)
        pnl_data.append({
            'symbol': symbol,
            'pnl': pnl,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    log_pnl_to_file(pnl_data)


def log_pnl_to_file(pnl_data, filename="pnl_log.csv"):
    """Log PnL data to a CSV file in the 'pnl' folder with a timestamped filename."""

    # Define the directory path
    directory = 'pnl'

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    # Append the timestamp to the filename
    filename = f"pnl_log_{timestamp}.csv"

    # Define the full file path
    filepath = os.path.join(directory, filename)

    # Create a DataFrame and save it to the CSV file
    df = pd.DataFrame(pnl_data)
    df.to_csv(filepath, mode='a', header=False, index=False)
    print(f"PnL data logged to {filepath}")


def reconcile_positions_and_orders():
    """Ensure that the bot's internal state aligns with actual account state."""
    current_positions = get_current_positions()
    open_orders = get_orders_by_status(['open', 'accepted', 'pending_new', 'partially_filled'])
    return current_positions, open_orders


def check_pnl_and_decide(symbol, total_pnl, adjusted_target_profit, adjusted_stop_loss):
    """
    Check total PnL and decide whether to hold, buy, or sell.

    Parameters:
    - symbol: The stock symbol.
    - total_pnl: The total profit or loss for the position.
    - adjusted_target_profit: The dynamically adjusted profit target.
    - adjusted_stop_loss: The dynamically adjusted stop loss limit.

    Returns:
    - 'sell' if the position should be sold.
    - 'hold' if the position should be held.
    """
    if total_pnl >= adjusted_target_profit:
        log_message(f"{symbol}: Adjusted target profit of ${adjusted_target_profit} reached. Selling position.",
                    level=logging.INFO)
        return 'sell'
    elif total_pnl <= adjusted_stop_loss:
        log_message(f"{symbol}: Adjusted stop loss of ${adjusted_stop_loss} reached. Selling position.",
                    level=logging.INFO)
        return 'sell'
    else:
        log_message(f"{symbol}: Holding position. No action required.", level=logging.INFO)
        return 'hold'


def calculate_historical_volatility(symbol, data, lookback_period=30):
    """
    Calculate the historical volatility of a stock based on its closing prices.

    :param symbol: The stock symbol
    :param data: List of historical price bars (assumed to be in chronological order)
    :param lookback_period: Number of days to calculate volatility over
    :return: The historical volatility as a percentage
    """
    closing_prices = np.array([bar._raw['c'] for bar in data])  # Access the closing price through _raw
    if len(closing_prices) < lookback_period:
        log_message(f"{symbol}: Not enough data points to calculate historical volatility.", level=logging.WARNING)
        return None

    # Calculate daily returns
    returns = np.diff(closing_prices) / closing_prices[:-1]

    # Calculate standard deviation of returns (historical volatility)
    volatility = np.std(returns[-lookback_period:]) * np.sqrt(252)  # Annualize the volatility

    log_message(f"<{symbol}>:Calculated historical volatility: {volatility:.2%}", level=logging.INFO)
    return volatility


def main():
    log_message("Starting trading bot")

    strategy = moving_average_crossover
    # 1Day, 1Hour, 1Min, 1Sec
    timeframe = '1Min'

    # Initialize Risk Manager with risk_percentage
    risk_manager = RiskManager(
        max_loss_per_trade=5,  # 2% of $250
        max_daily_loss=12.5,  # 5% of $250
        initial_capital=250,  # Account balance
        risk_percentage=5  # 5% risk per trade
    )

    target_profit = 7.5  # Adjusted target profit
    stop_loss_limit = -5  # Adjusted stop loss limit

    try:
        while True:

            # Check the current time (in EST)
            current_time = datetime.now().astimezone().strftime('%H:%M')
            market_close_time = '16:00'  # 4:00 PM EST

            if current_time >= market_close_time:
                log_message("Market is closed. Stopping trading bot.", level=logging.INFO)
                break  # Exit the loop to stop the bot

            # Reconcile positions and orders at the start of each iteration
            current_positions, open_orders = reconcile_positions_and_orders()

            monitor_pnl(current_positions)  # Monitor PnL for current positions

            all_data = fetch_live_data_for_all_symbols(timeframe)
            for symbol, data in all_data.items():
                if data:
                    # Calculate Historical Volatility
                    historical_volatility = calculate_historical_volatility(symbol, data, lookback_period=30)
                    if historical_volatility is None:
                        continue  # Skip this symbol if we couldn't calculate volatility

                    # Adjust stop-loss and profit targets based on volatility
                    adjusted_stop_loss = stop_loss_limit * (1 + historical_volatility)
                    adjusted_target_profit = target_profit * (1 + historical_volatility)

                    # Run the strategy and generate orders
                    orders = strategy(risk_manager, data, symbol)

                    # Place and handle orders
                    for order in orders:
                        # Check for existing open or pending orders for the symbol
                        existing_orders = open_orders.get(symbol, [])
                        if existing_orders:
                            for existing_order in existing_orders:
                                log_message(f"Existing orders for {symbol}: {[o.id for o in existing_orders]}",
                                            level=logging.INFO)

                                # If the existing order's quantity differs from the new one, modify or replace it
                                if existing_order.qty != order['qty']:
                                    modify_or_replace_order(existing_order, order['qty'], risk_manager)
                                continue
                        if order['side'] == 'buy':
                            position_qty = current_positions.get(symbol, 0)
                            if position_qty > 0:
                                log_message(f"Already holding {position_qty} shares of {symbol}. Skipping buy order.",
                                            level=logging.INFO)
                                continue
                            placed_order = place_order(order['symbol'], order['qty'], order['side'],
                                                       risk_manager=risk_manager)
                            handle_order_execution(placed_order, order['symbol'], risk_manager)
                        elif order['side'] == 'sell':
                            position_qty = current_positions.get(symbol, 0)
                            if position_qty <= 0:
                                log_message(f"No holdings of {symbol} to sell. Skipping sell order.",
                                            level=logging.INFO)
                                continue

                            # Calculate total PnL for the position
                            entry_price = float(api.get_position(symbol).avg_entry_price)
                            current_price = float(api.get_latest_trade(symbol).price)
                            total_pnl = calculate_pnl(symbol, entry_price, current_price, position_qty)

                            # Decide whether to sell based on the total PnL
                            action = check_pnl_and_decide(symbol, total_pnl, adjusted_target_profit, adjusted_stop_loss)
                            if action == 'sell':
                                sell_qty = min(order['qty'], position_qty)
                                placed_order = place_order(order['symbol'], sell_qty, order['side'],
                                                           risk_manager=risk_manager)
                                handle_order_execution(placed_order, order['symbol'], risk_manager)

                                # Record the trade in the PerformanceTracker
                                performance_tracker.record_trade(symbol, sell_qty, current_price, 'sell', total_pnl)

            time.sleep(60)
    except Exception as e:
        log_message(f"Error in trading bot: {str(e)}", level=logging.ERROR)
    finally:
        # Save performance metrics at the end of the trading session
        performance_tracker.save_metrics()


if __name__ == "__main__":
    main()
