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


def reconcile_positions_and_orders():
    """
    Ensures that the bot's internal state aligns with actual account state.
    """
    current_positions = get_current_positions()
    open_orders = get_orders_by_status(['open', 'accepted', 'pending_new', 'partially_filled'])
    return current_positions, open_orders


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
        while True:
            # Reconcile positions and orders at the start of each iteration
            current_positions, open_orders = reconcile_positions_and_orders()

            all_data = fetch_live_data_for_all_symbols(timeframe)  # Use the live data fetching function
            for symbol, data in all_data.items():
                if data:
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
                                continue  # Skip placing a new order if there are existing ones

                        if order['side'] == 'buy':
                            position_qty = current_positions.get(symbol, 0)
                            if position_qty > 0:
                                log_message(f"Already holding {position_qty} shares of {symbol}. Skipping buy order.",
                                            level=logging.INFO)
                                continue  # Skip if already holding position
                            placed_order = place_order(order['symbol'], order['qty'], order['side'],
                                                       risk_manager=risk_manager)
                            handle_order_execution(placed_order, order['symbol'], risk_manager)
                        elif order['side'] == 'sell':
                            position_qty = current_positions.get(symbol, 0)
                            if position_qty <= 0:
                                log_message(f"No holdings of {symbol} to sell. Skipping sell order.",
                                            level=logging.INFO)
                                continue  # Skip if no holdings to sell
                            # Ensure not to sell more than holdings
                            sell_qty = min(order['qty'], position_qty)
                            placed_order = place_order(order['symbol'], sell_qty, order['side'],
                                                       risk_manager=risk_manager)
                            handle_order_execution(placed_order, order['symbol'], risk_manager)

            time.sleep(60)  # Wait for the next minute's data
    except Exception as e:
        log_message(f"Error in trading bot: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
