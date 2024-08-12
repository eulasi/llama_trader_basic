import numpy as np
from utils.data_fetcher import fetch_data_for_all_symbols
from utils.logger import log_message


def mean_reversion():
    log_message("Executing mean reversion strategy")

    all_data = fetch_data_for_all_symbols('day')
    orders = []

    for symbol, data in all_data.items():
        if not data:
            continue

        closing_prices = [bar.close for bar in data]
        mean_price = np.mean(closing_prices)
        current_price = closing_prices[-1]

        if current_price < mean_price * 0.95:
            log_message(
                f"{symbol}: Current ({current_price}) is below mean price ({mean_price}). Generating a buy order.")
            orders.append({'symbol': symbol, 'qty': 1, 'side': 'buy'})
        elif current_price > mean_price * 1.05:
            log_message(
                f"{symbol}: Current ({current_price}) is above mean price ({mean_price}). Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': 1, 'side': 'sell'})
        else:
            log_message(f"{symbol}: Current price is near the mean price. No order generated.")

    return orders
