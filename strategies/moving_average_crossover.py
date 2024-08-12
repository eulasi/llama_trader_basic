import logging

import numpy as np
from utils.data_fetcher import fetch_data_for_all_symbols
from utils.logger import log_message


def moving_average_crossover(risk_manager, short_window=10, long_window=30, volatility_adjustment=True):
    log_message("Executing moving average crossover strategy")

    all_data = fetch_data_for_all_symbols('day')
    orders = []

    for symbol, data in all_data.items():
        if not data:
            continue

        closing_prices = [bar.close for bar in data]

        # Ensure there are enough data points for the moving averages
        if len(closing_prices) < long_window:
            log_message(f"{symbol}: Not enough data points to calculate moving averages. Skipping.",
                        level=logging.WARNING)
            continue

        short_ma = np.mean(closing_prices[-short_window:])
        long_ma = np.mean(closing_prices[-long_window:])  # Correctly use long_window

        # Calculate order quantity based on risk management and volatility
        symbol_price = closing_prices[-1]
        order_qty = risk_manager.calculate_position_size(symbol_price)

        if volatility_adjustment:
            # Adjust position size based on volatility (e.g., standard deviation of price changes)
            volatility = np.std(closing_prices)
            max_volatility = 0.02  # Example max volatility threshold (2%)
            if volatility > max_volatility:
                order_qty *= max_volatility / volatility  # Reduce size for more volatile stocks

        if short_ma > long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is above Long MA ({long_ma}). Generating a buy order.")
            orders.append({'symbol': symbol, 'qty': int(order_qty), 'side': 'buy'})
        elif short_ma < long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is below Long MA ({long_ma}). Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': int(order_qty), 'side': 'sell'})
        else:
            log_message(f"{symbol}: Short MA is equal to Long MA. No order generated.")

    return orders
