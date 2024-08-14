import logging

import numpy as np
from utils.logger import log_message


def moving_average_crossover(risk_manager, data, short_window=10, long_window=30, volatility_adjustment=True):
    log_message("Executing moving average crossover strategy")

    orders = []

    closing_prices = [bar._raw['c'] for bar in data]  # Access the closing price through _raw

    # Ensure there are enough data points for the moving averages
    if len(closing_prices) < long_window:
        log_message(f"Not enough data points to calculate moving averages. Skipping.", level=logging.WARNING)
        return orders

    short_ma = np.mean(closing_prices[-short_window:])
    long_ma = np.mean(closing_prices[-long_window:])

    # Calculate order quantity based on risk management and volatility
    symbol_price = closing_prices[-1]
    order_qty = risk_manager.calculate_position_size(symbol_price) if risk_manager else 1

    if volatility_adjustment:
        # Adjust position size based on volatility (e.g., standard deviation of price changes)
        volatility = np.std(closing_prices)
        max_volatility = 0.02  # Example max volatility threshold (2%)
        log_message(f"Calculated volatility: {volatility}, Max volatility threshold: {max_volatility}")
        if volatility > max_volatility:
            adjusted_qty = int(order_qty * max_volatility / volatility)
            log_message(f"Adjusting order quantity due to volatility. New quantity: {adjusted_qty}")
            order_qty = adjusted_qty

    if order_qty > 0:
        if short_ma > long_ma:
            log_message(f"Short MA ({short_ma}) is above Long MA ({long_ma}). Generating a buy order.")
            orders.append({'symbol': data[0]._raw['S'], 'qty': order_qty, 'side': 'buy'})
        elif short_ma < long_ma:
            log_message(f"Short MA ({short_ma}) is below Long MA ({long_ma}). Generating a sell order.")
            orders.append({'symbol': data[0]._raw['S'], 'qty': order_qty, 'side': 'sell'})
        else:
            log_message("Short MA is equal to Long MA. No order generated.")
    else:
        log_message("Final calculated order quantity is zero. No order generated.", level=logging.WARNING)

    return orders
