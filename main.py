import logging
import time
from strategies.moving_average_crossover import moving_average_crossover
from utils.live_data_fetcher import fetch_live_data_for_all_symbols
from utils.order_executor import place_order, handle_order_execution
from utils.logger import log_message
from utils.risk_management import RiskManager
import alpaca_trade_api as tradeapi
from config.credentials import API_KEY, API_SECRET, BASE_URL

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def get_current_positions():
    """Fetch current positions from Alpaca."""
    positions = api.list_positions()
    current_positions = {position.symbol: float(position.qty) for position in positions}
    return current_positions


def get_open_orders():
    """Fetch open orders from Alpaca."""
    open_orders = api.list_orders(status='open')
    open_orders_dict = {order.symbol: order for order in open_orders}
    return open_orders_dict


def main():
    log_message("Starting trading bot")

    strategy = moving_average_crossover
    # 1Day, 1Hour, 1Min, 1Sec
    timeframe = '1Min'

    # Initialize Risk Manager with risk_percentage
    risk_manager = RiskManager(
        max_loss_per_trade=100,
        max_daily_loss=500,
        initial_capital=10000,
        risk_percentage=20  # 20% risk per trade
    )

    try:
        # Fetch current positions and open orders
        current_positions = get_current_positions()
        open_orders = get_open_orders()

        while True:
            all_data = fetch_live_data_for_all_symbols(timeframe)  # Use the live data fetching function
            for symbol, data in all_data.items():
                if data:
                    # Run the strategy and generate orders
                    orders = strategy(risk_manager, data, symbol)

                    # Place and handle orders
                    for order in orders:
                        # Check if there's already an open order for the symbol
                        if symbol in open_orders:
                            log_message(f"Skipping new order for {symbol} as there is already an open order.",
                                        level=logging.WARNING)
                            continue

                        if order['side'] == 'buy' and symbol not in current_positions:
                            placed_order = place_order(order['symbol'], order['qty'], order['side'],
                                                       risk_manager=risk_manager)
                            handle_order_execution(placed_order, order['symbol'], risk_manager)
                        elif order['side'] == 'sell' and symbol in current_positions:
                            placed_order = place_order(order['symbol'], order['qty'], order['side'],
                                                       risk_manager=risk_manager)
                            handle_order_execution(placed_order, order['symbol'], risk_manager)

            # Refresh open orders list after each iteration
            open_orders = get_open_orders()

            time.sleep(60)  # Wait for the next minute's data
    except Exception as e:
        log_message(f"Error in trading bot: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
