import logging
import time
from config.credentials import API_KEY, API_SECRET, BASE_URL
import alpaca_trade_api as tradeapi
from utils.risk_management import RiskManager
from utils.logger import log_message

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Initialize Risk Manager
initial_capital = 10000  # This can be dynamically set based on your needs
risk_manager = RiskManager(max_loss_per_trade=100, max_daily_loss=500, initial_capital=initial_capital)


def place_order(symbol, qty, side, order_type='market', time_in_force='day'):
    try:
        latest_trade = api.get_latest_trade(symbol)
        if latest_trade is None:
            log_message(f"Failed to retrieve the latest trade for {symbol}. Order not placed.", level=logging.ERROR)
            return None

        symbol_price = latest_trade.price
        position_size = risk_manager.calculate_position_size(symbol_price)

        if qty > position_size:
            log_message(f"Reducing position size for {symbol}. Max allowed: {position_size}")
            qty = position_size

        if side == 'sell':
            try:
                current_position = api.get_position(symbol)
                if float(current_position.qty) < qty:
                    log_message(f"Reducing sell size for {symbol}. Max allowed: {current_position.qty}")
                    qty = float(current_position.qty)
            except Exception as e:
                log_message(f"Failed to retrieve current position for {symbol}: {str(e)}", level=logging.ERROR)
                return None

        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
        log_message(f"Order placed for {symbol}: {side} {qty} shares at {symbol_price} each.")
        return order

    except tradeapi.rest.APIError as api_err:
        log_message(f"API Error when placing order for {symbol}: {str(api_err)}", level=logging.ERROR)
        time.sleep(10)  # Handle rate limit or temporary issues with a delay
        return None

    except Exception as e:
        log_message(f"Failed to place order for {symbol}: {str(e)}", level=logging.ERROR)
        return None


def handle_order_execution(order, symbol):
    if order is None:
        log_message(f"No order to execute for {symbol}.", level=logging.WARNING)
        return False

    try:
        status = order.status
        filled_qty = float(order.filled_qty)
        latest_trade = api.get_latest_trade(symbol)
        if latest_trade is None:
            log_message(f"Failed to retrieve the latest trade for {symbol}. Cannot calculate PnL.", level=logging.ERROR)
            return False

        symbol_price = latest_trade.price
        realized_pnl = 0  # Initialize realized_pnl to zero

        if status == 'filled':
            if order.side == 'sell':
                # PnL should consider the difference between buy price and sell price
                average_buy_price = float(api.get_position(symbol).avg_entry_price)
                realized_pnl = filled_qty * (symbol_price - average_buy_price)
                if not risk_manager.update_daily_loss(realized_pnl):
                    log_message("Daily loss limit exceeded, halting trading.")
                    return False

            # Update capital only if the order is filled
            risk_manager.update_capital(realized_pnl)

        log_message(f"Order executed: {status} for {symbol}, Realized PnL: ${realized_pnl:.2f}")
        return True

    except tradeapi.rest.APIError as api_err:
        log_message(f"API Error during order execution for {symbol}: {str(api_err)}", level=logging.ERROR)
        time.sleep(10)  # Handle rate limit or temporary issues with a delay
        return False

    except Exception as e:
        log_message(f"Failed to execute order for {symbol}: {str(e)}", level=logging.ERROR)
        return False
