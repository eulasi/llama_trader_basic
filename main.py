import logging

from strategies.moving_average_crossover import moving_average_crossover
from strategies.mean_reversion import mean_reversion
from utils.logger import log_message
from utils.order_executor import handle_order_execution, place_order


def main():
    try:
        log_message("Starting trading bot")

        # Select the strategy you want to test
        strategy = moving_average_crossover  # or mean_reversion

        # Execute the strategy and get the orders to be placed
        orders = strategy()

        # Process each order returned by the strategy
        for order in orders:
            placed_order = place_order(order['symbol'], order['qty'], order['side'])
            if not handle_order_execution(placed_order, order['symbol']):
                break  # Stop if daily loss limit is exceeded

        log_message("Trading bot finished execution")

    except Exception as e:
        log_message(f"Error: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
