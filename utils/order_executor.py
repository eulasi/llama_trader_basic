from config.credentials import API_KEY, API_SECRET, BASE_URL
import alpaca_trade_api as tradeapi

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def place_order(symbol, qty, side, order_type='market', time_in_force='gtc'):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=order_type,
        time_in_force=time_in_force
    )
