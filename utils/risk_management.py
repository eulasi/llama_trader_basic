from utils.logger import log_message


class RiskManager:
    def __init__(self, max_loss_per_trade, max_daily_loss, initial_capital):
        self.max_loss_per_trade = max_loss_per_trade
        self.max_daily_loss = max_daily_loss
        self.initial_capital = initial_capital
        self.daily_loss = 0

    def calculate_position_size(self, symbol_price):
        # Risk a fixed percentage of capital per trade
        risk_per_trade = self.max_loss_per_trade
        position_size = risk_per_trade / symbol_price
        return position_size

    def update_daily_loss(self, loss):
        self.daily_loss += loss
        if self.daily_loss > self.max_daily_loss:
            log_message("Maximum daily loss exceeded. Stopping trading for today.")
            return False
        return True

    def reset_daily_loss(self):
        self.daily_loss = 0
