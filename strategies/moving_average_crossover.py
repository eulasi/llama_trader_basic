import logging

import numpy as np
from utils.logger import log_message


def moving_average_crossover(risk_manager, data, symbol, short_window=10, long_window=30, min_volatility=0.5,
                             max_volatility=50.0, volatility_adjustment=True):
    log_message(f"Executing moving average crossover strategy for {symbol}")

    orders = []

    closing_prices = [bar._raw['c'] for bar in data]  # Access the closing price through _raw

    # Ensure there are enough data points for the moving averages
    if len(closing_prices) < long_window:
        log_message(f"{symbol}: Not enough data points to calculate moving averages. Skipping.", level=logging.WARNING)
        return orders

    short_ma = np.mean(closing_prices[-short_window:])
    long_ma = np.mean(closing_prices[-long_window:])

    # Calculate volatility
    volatility = np.std(closing_prices)
    log_message(f"Calculated volatility: {volatility}")

    # Dynamic Volatility Check
    if volatility < min_volatility:
        log_message(f"Volatility {volatility} is too low. Skipping trading.", level=logging.WARNING)
        return orders
    elif volatility > max_volatility:
        log_message(f"Volatility {volatility} is high but within acceptable range. Proceeding with caution.",
                    level=logging.WARNING)

        if volatility_adjustment:
            # Adjust position size based on volatility
            order_qty = risk_manager.calculate_position_size(closing_prices[-1]) if risk_manager else 1
            adjusted_qty = int(order_qty * (max_volatility / volatility))
            log_message(f"Adjusting order quantity due to high volatility. New quantity: {adjusted_qty}")
            order_qty = adjusted_qty
        else:
            order_qty = risk_manager.calculate_position_size(closing_prices[-1]) if risk_manager else 1
    else:
        # Normal trading conditions
        order_qty = risk_manager.calculate_position_size(closing_prices[-1]) if risk_manager else 1

    if order_qty > 0:
        if short_ma > long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is above Long MA ({long_ma}). Generating a buy order.")
            orders.append({'symbol': symbol, 'qty': order_qty, 'side': 'buy'})
        elif short_ma < long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is below Long MA ({long_ma}). Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': order_qty, 'side': 'sell'})
        else:
            log_message(f"{symbol}: Short MA is equal to Long MA. No order generated.")
    else:
        log_message(f"{symbol}: Final calculated order quantity is zero. No order generated.", level=logging.WARNING)

    return orders
