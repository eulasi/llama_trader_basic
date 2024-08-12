import logging

from config.credentials import API_KEY, API_SECRET, BASE_URL
import alpaca_trade_api as tradeapi
from utils.risk_management import RiskManager
from utils.logger import log_message

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Initialize Risk Manager
initial_capital = 10000  # Example initial capital
risk_manager = RiskManager(max_loss_per_trade=100, max_daily_loss=500, initial_capital=initial_capital)


def place_order(symbol, qty, side, order_type='market', time_in_force='day'):
    symbol_price = api.get_latest_trade(symbol).price
    position_size = risk_manager.calculate_position_size(symbol_price)

    if qty > position_size:
        log_message(f"Reducing position size for {symbol}. Max allowed: {position_size}")
        qty = position_size

    if side == 'sell':
        current_position = api.get_position(symbol)
        if float(current_position.qty) < qty:
            log_message(f"Reducing sell size for {symbol}. Max allowed: {current_position.qty}")
            qty = float(current_position.qty)

    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
        log_message(f"Order placed for {symbol}: {side} {qty} shares at {symbol_price} each.")
        return order
    except Exception as e:
        log_message(f"Failed to place order for {symbol}: {str(e)}", level=logging.ERROR)


def handle_order_execution(order, symbol):
    if order:
        status = order.status
        filled_qty = float(order.filled_qty)
        symbol_price = api.get_latest_trade(symbol).price

        realized_pnl = 0  # Initialize realized_pnl to zero or a default value

        if status == 'filled':
            if order.side == 'sell':
                realized_pnl = filled_qty * symbol_price  # Simplified PnL calculation
                if not risk_manager.update_daily_loss(realized_pnl):
                    log_message("Daily loss limit exceeded, halting trading.")
                    return False
            # Update capital only if the order is filled
            risk_manager.update_capital(realized_pnl)

        log_message(f"Order executed: {status} for {symbol}")
    return True
