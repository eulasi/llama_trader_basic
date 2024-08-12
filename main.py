import logging
import time
from strategies.moving_average_crossover import moving_average_crossover
from utils.live_data_fetcher import fetch_live_data_for_all_symbols
from utils.order_executor import place_order
from utils.logger import log_message


def run_paper_trading():
    # Set the timeframe for live trading
    timeframe = '1Min'
    strategy = moving_average_crossover

    while True:
        all_data = fetch_live_data_for_all_symbols(timeframe)  # Use the live data fetching function
        orders = strategy(all_data)
        for order in orders:
            place_order(order['symbol'], order['qty'], order['side'])
        time.sleep(60)  # Wait for the next minute's data


def main():
    log_message("Starting paper trading bot")
    try:
        run_paper_trading()
    except Exception as e:
        log_message(f"Error in paper trading bot: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
