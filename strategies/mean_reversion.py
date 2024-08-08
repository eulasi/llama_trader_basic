import numpy as np
from utils.data_fetcher import get_historical_data
from utils.order_executor import place_order
from utils.logger import log_message
from config.config import TRADING_SYMBOL


def mean_reversion():
    log_message("Executing mean reversion strategy")

    data = get_historical_data(TRADING_SYMBOL, 'day', limit=30)
    closing_prices = [bar.c for bar in data]
    mean_price = np.mean(closing_prices)
    current_price = closing_prices[-1]

    if current_price < mean_price * 0.95:
        log_message(f"Current price ({current_price}) is below mean price ({mean_price}). Placing a buy order.")
        place_order(TRADING_SYMBOL, 1, 'buy')
    elif current_price > mean_price * 1.05:
        log_message(f"Current price ({current_price}) is above mean price ({mean_price}). Placing a sell order.")
        place_order(TRADING_SYMBOL, 1, 'sell')
    else:
        log_message("Current price is near the mean price. No action taken.")
