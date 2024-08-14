import os
import pandas as pd
import logging


class PerformanceTracker:
    def __init__(self):
        self.trades = []
        self.total_pnl = 0
        self.win_count = 0
        self.loss_count = 0
        self.max_drawdown = 0
        self.current_peak = 0

        # Ensure the performance_data directory exists within the data folder
        self.metrics_directory = os.path.join('data', 'performance_data')
        if not os.path.exists(self.metrics_directory):
            os.makedirs(self.metrics_directory)
            logging.info(f"Created metrics directory: {self.metrics_directory}")

    def record_trade(self, symbol, qty, price, side, pnl):
        try:
            self.trades.append({
                'symbol': symbol,
                'qty': qty,
                'price': price,
                'side': side,
                'pnl': pnl
            })
            self.total_pnl += pnl

            if pnl > 0:
                self.win_count += 1
            elif pnl < 0:
                self.loss_count += 1

            self.update_drawdown()
            # Log each trade recorded
            logging.info(f"Recorded trade for {symbol}: {side} {qty} shares at {price} each, PnL: {pnl}")
        except Exception as e:
            logging.error(f"Failed to record trade: {str(e)}")

    def update_drawdown(self):
        try:
            if self.total_pnl > self.current_peak:
                self.current_peak = self.total_pnl
            drawdown = self.current_peak - self.total_pnl
            if drawdown > self.max_drawdown:
                self.max_drawdown = drawdown
        except Exception as e:
            logging.error(f"Failed to update drawdown: {str(e)}")

    def get_metrics(self):
        total_trades = self.win_count + self.loss_count
        win_rate = (self.win_count / total_trades) * 100 if total_trades > 0 else 0
        avg_return_per_trade = self.total_pnl / total_trades if total_trades > 0 else 0

        return {
            'total_pnl': self.total_pnl,
            'win_rate': win_rate,
            'avg_return_per_trade': avg_return_per_trade,
            'max_drawdown': self.max_drawdown,
            'total_trades': total_trades
        }

    def save_metrics(self, filename=None):
        try:
            if filename is None:
                filename = f"performance_metrics_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            metrics_df = pd.DataFrame(self.trades)
            filepath = os.path.join(self.metrics_directory, filename)
            metrics_df.to_csv(filepath, index=False)
            logging.info(f"Performance metrics saved to {filepath}")
        except Exception as e:
            logging.error(f"Failed to save performance metrics: {str(e)}")

    def reset(self):
        self.trades = []
        self.total_pnl = 0
        self.win_count = 0
        self.loss_count = 0
        self.max_drawdown = 0
        self.current_peak = 0
