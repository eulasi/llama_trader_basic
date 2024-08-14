import logging
import time
from strategies.moving_average_crossover import moving_average_crossover
from utils.live_data_fetcher import fetch_live_data_for_all_symbols
from utils.order_executor import place_order
from utils.logger import log_message
from utils.risk_management import RiskManager
from config.symbols import symbol_list  # Assuming symbol_list is defined here


def main():
    log_message("Starting trading bot")

    # Instantiate the RiskManager
    risk_manager = RiskManager(
        max_loss_per_trade=50,  # Example value, adjust as needed
        max_daily_loss=100,  # Example value, adjust as needed
        initial_capital=250,  # Should match the initial cash used in the backtest
        risk_percentage=1  # 1% risk per trade
    )

    strategy = moving_average_crossover
    # Set the trading timeframe
    timeframe = '1Min'

    try:
        while True:
            # Fetch live data for all symbols
            all_data = fetch_live_data_for_all_symbols(timeframe)

            # Loop through each symbol and apply the strategy
            for symbol in symbol_list:
                symbol_data = all_data.get(symbol)
                if symbol_data:
                    # Call the strategy function with the required arguments
                    orders = strategy(risk_manager, symbol_data, symbol)

                    # Place the orders
                    for order in orders:
                        place_order(order['symbol'], order['qty'], order['side'])

            # Wait for the next minute's data
            time.sleep(60)
    except Exception as e:
        log_message(f"Error in trading bot: {str(e)}", level=logging.ERROR)


if __name__ == "__main__":
    main()
