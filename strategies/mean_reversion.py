import numpy as np
from utils.data_fetcher import fetch_data_for_all_symbols
from utils.logger import log_message
from utils.risk_management import RiskManager


def mean_reversion(risk_manager, buy_threshold=0.95, sell_threshold=1.05, volatility_adjustment=True):
    log_message("Executing mean reversion strategy")

    all_data = fetch_data_for_all_symbols('day')
    orders = []

    for symbol, data in all_data.items():
        if not data:
            continue

        closing_prices = [bar.close for bar in data]
        mean_price = np.mean(closing_prices)
        current_price = closing_prices[-1]

        # Calculate order quantity based on risk management and volatility
        symbol_price = current_price
        order_qty = risk_manager.calculate_position_size(symbol_price)

        if volatility_adjustment:
            # Adjust position size based on volatility (e.g., standard deviation of price changes)
            volatility = np.std(closing_prices)
            max_volatility = 0.02  # Example max volatility threshold (2%)
            if volatility > max_volatility:
                order_qty *= max_volatility / volatility  # Reduce size for more volatile stocks

        if current_price < mean_price * buy_threshold:
            log_message(
                f"{symbol}: Current ({current_price}) is below mean price ({mean_price}). Generating a buy order.")
            orders.append({'symbol': symbol, 'qty': int(order_qty), 'side': 'buy'})
        elif current_price > mean_price * sell_threshold:
            log_message(
                f"{symbol}: Current ({current_price}) is above mean price ({mean_price}). Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': int(order_qty), 'side': 'sell'})
        else:
            log_message(f"{symbol}: Current price is near the mean price. No order generated.")

    return orders
