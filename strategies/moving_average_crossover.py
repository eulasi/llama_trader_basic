import logging
import numpy as np
from utils.data_fetcher import fetch_data_for_all_symbols, convert_timeframe
from utils.logger import log_message


def moving_average_crossover(risk_manager, short_window=10, long_window=30, volatility_adjustment=True):
    log_message("Executing moving average crossover strategy")

    # Convert 'day' string to TimeFrame object
    timeframe = convert_timeframe('1Day')
    all_data = fetch_data_for_all_symbols(timeframe)
    orders = []

    for symbol, data in all_data.items():
        if not data:
            log_message(f"{symbol}: No data fetched. Skipping.", level=logging.WARNING)
            continue

        # Access the closing prices using the _raw attribute
        closing_prices = [bar._raw['c'] for bar in data]
        log_message(f"{symbol}: Fetched {len(closing_prices)} data points.")

        # Log each bar's date and close price to inspect the data
        for bar in data:
            log_message(f"Date: {bar._raw['t']}, Close: {bar._raw['c']}")

        # Ensure there are enough data points for the moving averages
        if len(closing_prices) < long_window:
            log_message(f"{symbol}: Not enough data points to calculate moving averages. Skipping.",
                        level=logging.WARNING)
            continue

        short_ma = np.mean(closing_prices[-short_window:])
        long_ma = np.mean(closing_prices[-long_window:])

        # Calculate order quantity based on risk management
        symbol_price = closing_prices[-1]
        order_qty = risk_manager.calculate_position_size(symbol_price)

        if order_qty <= 0:
            log_message(f"{symbol}: Calculated order quantity is zero. Skipping order generation.",
                        level=logging.WARNING)
            continue

        if volatility_adjustment:
            # Adjust position size based on volatility (e.g., standard deviation of price changes)
            volatility = np.std(closing_prices)
            max_volatility = 0.02  # Example max volatility threshold (2%)
            if volatility > max_volatility:
                adjusted_qty = int(order_qty * max_volatility / volatility)
                log_message(f"{symbol}: Adjusting order quantity due to volatility. New quantity: {adjusted_qty}")
                order_qty = adjusted_qty

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
            log_message(f"{symbol}: Final calculated order quantity is zero. No order generated.",
                        level=logging.WARNING)

    return orders
