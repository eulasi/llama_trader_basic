import numpy as np
from utils.data_fetcher import get_historical_data
from utils.order_executor import place_order
from utils.logger import log_message
from config.config import SHORT_WINDOW, LONG_WINDOW, TRADING_SYMBOL

def moving_average_crossover():
    log_message("Executing moving average crossover strategy")

    data = get_historical_data(TRADING_SYMBOL, 'day', LONG_WINDOW)
    closing_prices = [bar.c for bar in data]

    short_ma = np.mean(closing_prices[-SHORT_WINDOW:])
    long_ma = np.mean(closing_prices)

    if short_ma > long_ma:
        log_message(f"Short MA ({short_ma}) is above Long MA ({long_ma}). Placing a buy order.")
        place_order(TRADING_SYMBOL, 1, 'buy')
    elif short_ma < long_ma:
        log_message(f"Short MA ({short_ma}) is below Long MA ({long_ma}). Placing a sell order.")
        place_order(TRADING_SYMBOL, 1, 'sell')
    else:
        log_message("Short MA is equal to Long MA. No action taken.")
