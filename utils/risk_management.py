import logging
from utils.logger import log_message


class RiskManager:
    def __init__(self, max_loss_per_trade, max_daily_loss, initial_capital, risk_percentage=1):
        self.max_loss_per_trade = max_loss_per_trade
        self.max_daily_loss = max_daily_loss
        self.initial_capital = initial_capital
        self.risk_percentage = risk_percentage / 100
        self.daily_loss = 0
        self.current_capital = initial_capital
        self.max_drawdown = 0
        self.current_peak = initial_capital

    def calculate_position_size(self, symbol_price):
        if symbol_price <= 0:
            log_message(f"Invalid symbol price: {symbol_price}. Cannot calculate position size.", level=logging.ERROR)
            return 0  # Return 0 to indicate no position should be taken

        risk_per_trade = self.current_capital * self.risk_percentage
        position_size = risk_per_trade / symbol_price

        if position_size < 1:  # Ensuring a minimum position size of 1 share
            log_message(f"Calculated position size for {symbol_price} is less than 1. Adjusting to minimum size of 1.",
                        level=logging.WARNING)
            return 1

        return position_size

    def update_daily_loss(self, loss):
        self.daily_loss += loss
        if self.daily_loss > self.max_daily_loss:
            log_message("Maximum daily loss exceeded. Stopping trading for today.")
            return False
        return True

    def reset_daily_loss(self):
        self.daily_loss = 0

    def update_capital(self, realized_pnl):
        self.current_capital += realized_pnl
        log_message(f"Updated capital: {self.current_capital}")
        self.update_drawdown()

    def update_drawdown(self):
        if self.current_capital > self.current_peak:
            self.current_peak = self.current_capital
        drawdown = self.current_peak - self.current_capital
        if drawdown > self.max_drawdown:
            self.max_drawdown = drawdown
            log_message(f"New maximum drawdown: {self.max_drawdown}")

    def reset_capital(self):
        self.current_capital = self.initial_capital
        log_message(f"Capital reset to initial value: {self.initial_capital}")
