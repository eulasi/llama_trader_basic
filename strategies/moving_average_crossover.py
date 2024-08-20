import logging
import numpy as np
from utils.logger import log_message


def moving_average_crossover(risk_manager, data, symbol, short_window=10, long_window=30, min_volatility=0.5,
                             max_volatility=50.0, volatility_adjustment=True, profit_threshold=1.015,
                             stop_loss_threshold=0.975, trailing_stop_loss=0.98):
    log_message(f"Executing moving average crossover strategy for {symbol}")

    orders = []

    closing_prices = np.array([bar._raw['c'] for bar in data])  # Access the closing price through _raw

    # Ensure there are enough data points for the moving averages
    if len(closing_prices) < long_window:
        log_message(f"{symbol}: Not enough data points to calculate moving averages. Skipping.", level=logging.WARNING)
        return orders

    short_ma = np.mean(closing_prices[-short_window:])
    long_ma = np.mean(closing_prices[-long_window:])
    current_price = closing_prices[-1]

    # Calculate volatility and convert to percentage
    volatility = np.std(closing_prices)
    volatility_percentage = volatility * 100
    log_message(f"Calculated volatility: {volatility_percentage:.2f}%", level=logging.INFO)

    # Adjust position size based on volatility (if necessary)
    order_qty = risk_manager.calculate_position_size(current_price) if risk_manager else 1

    if order_qty == 0:
        log_message(f"{symbol}: Order quantity is zero due to risk management constraints. Skipping.",
                    level=logging.WARNING)
        return orders

    # Dynamic Volatility Check
    if volatility_percentage < min_volatility:
        log_message(f"Volatility {volatility_percentage:.2f}% is too low. Skipping trading.", level=logging.WARNING)
        return orders
    elif volatility_percentage > max_volatility:
        log_message(
            f"Volatility {volatility_percentage:.2f}% is high but within acceptable range. Proceeding with caution.",
            level=logging.WARNING)

        if volatility_adjustment:
            # Adjust position size based on volatility
            adjusted_qty = max(1, int(order_qty * (
                        max_volatility / volatility_percentage)))  # Ensure minimum order size of 1
            log_message(f"Adjusting order quantity due to high volatility. New quantity: {adjusted_qty}")
            order_qty = adjusted_qty

    # Adjust stop loss and profit targets based on volatility
    adjusted_stop_loss = current_price * stop_loss_threshold
    adjusted_target_profit = current_price * profit_threshold

    log_message(f"Adjusted Stop Loss for {symbol}: ${adjusted_stop_loss:.2f}", level=logging.INFO)
    log_message(f"Current Price for {symbol}: ${current_price:.2f}", level=logging.INFO)
    log_message(f"Adjusted Target Profit for {symbol}: ${adjusted_target_profit:.2f}", level=logging.INFO)

    # Apply trailing stop-loss logic
    trailing_stop_price = max(closing_prices) * trailing_stop_loss

    # Check for buy or sell signals
    if short_ma > long_ma:
        log_message(f"{symbol}: Short MA ({short_ma}) is above Long MA ({long_ma}). Generating a buy order.")
        orders.append({'symbol': symbol, 'qty': order_qty, 'side': 'buy'})
    elif short_ma < long_ma:
        if current_price <= trailing_stop_price:
            log_message(
                f"{symbol}: Current price ({current_price}) has dropped below the trailing stop price "
                f"({trailing_stop_price}). Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': order_qty, 'side': 'sell'})
        elif current_price >= closing_prices[0] * profit_threshold:
            log_message(
                f"{symbol}: Current price ({current_price}) exceeds the profit threshold. Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': order_qty, 'side': 'sell'})
        elif current_price <= closing_prices[0] * stop_loss_threshold:
            log_message(
                f"{symbol}: Current price "
                f"({current_price}) has dropped below the stop loss threshold. Generating a sell order.")
            orders.append({'symbol': symbol, 'qty': order_qty, 'side': 'sell'})
        else:
            log_message(f"{symbol}: No sell condition met. No order generated.")

    return orders
