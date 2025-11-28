from datetime import datetime

class RiskManager:
    def __init__(self, max_daily_trades, stop_loss_pct):
        self.max_daily_trades = max_daily_trades
        self.stop_loss_pct = stop_loss_pct
        self.daily_trades = 0
        self.last_trade_date = None

    def check_trade_allowed(self):
        current_date = datetime.now().date()
        if self.last_trade_date != current_date:
            self.daily_trades = 0
            self.last_trade_date = current_date
        
        if self.daily_trades >= self.max_daily_trades:
            return False
        return True

    def record_trade(self):
        self.daily_trades += 1

    def calculate_stop_loss(self, entry_price, side):
        if side == 'buy':
            return entry_price * (1 - self.stop_loss_pct)
        else:
            return entry_price * (1 + self.stop_loss_pct)
