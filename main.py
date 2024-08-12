import logging

from strategies.moving_average_crossover import moving_average_crossover
from strategies.mean_reversion import mean_reversion
from utils.logger import log_message
from utils.order_executor import handle_order_execution, place_order
from utils.performance_tracker import PerformanceTracker


def main():
    try:
        log_message("Starting trading bot")

        # Initialize the performance tracker
        performance_tracker = PerformanceTracker()

        # Select the strategy you want to test
        strategy = moving_average_crossover  # or mean_reversion

        # Execute the strategy and get the orders to be placed
        orders = strategy()

        # Process each order returned by the strategy
        for order in orders:
            placed_order = place_order(order['symbol'], order['qty'], order['side'])
            if placed_order and handle_order_execution(placed_order, order['symbol']):
                # Record trade details in the performance tracker
                symbol_price = placed_order.filled_avg_price
                pnl = order['qty'] * (symbol_price if order['side'] == 'sell' else -symbol_price)
                performance_tracker.record_trade(order['symbol'], order['qty'], symbol_price, order['side'], pnl)
            else:
                break  # Stop if daily loss limit is exceeded

        # Log performance metrics at the end of the trading session
        metrics = performance_tracker.get_metrics()
        log_message(f"Performance Metrics: {metrics}")

        # Optionally, save metrics to a CSV file for further analysis
        performance_tracker.save_metrics()

        log_message("Trading bot finished execution")

    except Exception as e:
        log_message(f"Error: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
