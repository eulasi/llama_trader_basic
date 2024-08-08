import numpy as np
from utils.data_fetcher import fetch_data_for_all_symbols
from utils.order_executor import place_order
from utils.logger import log_message

# Define constants here
SHORT_WINDOW = 10
LONG_WINDOW = 30


def moving_average_crossover():
    log_message("Executing moving average crossover strategy")

    all_data = fetch_data_for_all_symbols('day', LONG_WINDOW)

    for symbol, data in all_data.items():
        if not data:
            continue

        closing_prices = [bar.c for bar in data]
        short_ma = np.mean(closing_prices[-SHORT_WINDOW:])
        long_ma = np.mean(closing_prices)

        if short_ma > long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is above Long MA ({long_ma}). Placing a buy order.")
            place_order(symbol, 1, 'buy')
        elif short_ma < long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is below Long MA ({long_ma}). Placing a sell order.")
            place_order(symbol, 1, 'sell')
        else:
            log_message(f"{symbol}: Short MA is equal to Long MA. No action taken.")
