import logging

from strategies.moving_average_crossover import moving_average_crossover
from strategies.mean_reversion import mean_reversion
from utils.logger import log_message
from utils.order_executor import handle_order_execution, place_order
from utils.risk_management import RiskManager


def main():
    try:
        log_message("Starting trading bot")

        # Initialize the risk manager
        risk_manager = RiskManager(max_loss_per_trade=100, max_daily_loss=500, initial_capital=10000)

        # Choose the strategy to run and pass the risk manager
        orders = moving_average_crossover(risk_manager)  # Pass the risk manager to the strategy

        # Process each order returned by the strategy
        for order in orders:
            placed_order = place_order(order['symbol'], order['qty'], order['side'])
            if placed_order and handle_order_execution(placed_order, order['symbol']):
                continue
            else:
                break  # Stop if daily loss limit is exceeded

        log_message("Trading bot finished execution")

    except Exception as e:
        log_message(f"Error: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
