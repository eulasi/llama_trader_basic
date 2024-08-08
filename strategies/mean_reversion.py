import numpy as np
from utils.data_fetcher import fetch_data_for_all_symbols
from utils.order_executor import place_order
from utils.logger import log_message


def mean_reversion():
    log_message("Executing mean reversion strategy")

    all_data = fetch_data_for_all_symbols('day', 30)

    for symbol, data in all_data.items():
        if not data:
            continue

        closing_prices = [bar.c for bar in data]
        mean_price = np.mean(closing_prices)
        current_price = closing_prices[-1]

        if current_price < mean_price * 0.95:
            log_message(
                f"{symbol}: Current price ({current_price}) is below mean price ({mean_price}). Placing a buy order.")
            place_order(symbol, 1, 'buy')
        elif current_price > mean_price * 1.05:
            log_message(
                f"{symbol}: Current price ({current_price}) is above mean price ({mean_price}). Placing a sell order.")
            place_order(symbol, 1, 'sell')
        else:
            log_message(f"{symbol}: Current price is near the mean price. No action taken.")
