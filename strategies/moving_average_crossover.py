import numpy as np
from utils.data_fetcher import fetch_data_for_all_symbols
from utils.logger import log_message

SHORT_WINDOW = 10
LONG_WINDOW = 30


def moving_average_crossover():
    log_message("Executing moving average crossover strategy")

    all_data = fetch_data_for_all_symbols('day')
    orders = []

    for symbol, data in all_data.items():
        if not data:
            continue

        closing_prices = [bar.close for bar in data]
        short_ma = np.mean(closing_prices[-SHORT_WINDOW:])
        long_ma = np.mean(closing_prices)

        if short_ma > long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is above Long MA ({long_ma}). Generating a buy order.")
            orders.append({'symbol': symbol, 'qty': 1, 'side': 'buy'})
        elif short_ma < long_ma:
            log_message(f"{symbol}: Short MA ({short_ma}) is below Long MA ({long_ma}). Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': 1, 'side': 'sell'})
        else:
            log_message(f"{symbol}: Short MA is equal to Long MA. No order generated.")

    return orders
