import pandas as pd
from bot.strategy import Strategy
import config

class Backtester:
    def __init__(self, initial_balance=1000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.strategy = Strategy()
        self.trades = []

    def run(self, df):
        print("Starting backtest...")
        df = df.copy()
        
        # Generate signals
        # Note: In a real backtester, we'd iterate row by row to avoid lookahead bias
        # For simplicity/performance in this example, we'll iterate but use the strategy logic carefully
        
        position = None
        entry_price = 0
        
        for i in range(50, len(df)):
            current_slice = df.iloc[:i+1].copy()
            signal = self.strategy.generate_signal(current_slice)
            current_price = df.iloc[i]['close']
            timestamp = df.iloc[i]['timestamp']
            
            if position is None:
                if signal == 'buy':
                    position = 'long'
                    entry_price = current_price
                    self.trades.append({
                        'type': 'buy',
                        'price': entry_price,
                        'time': timestamp,
                        'balance': self.balance
                    })
                    print(f"Buy at {entry_price} on {timestamp}")
            
            elif position == 'long':
                if signal == 'sell':
                    position = None
                    exit_price = current_price
                    pnl = (exit_price - entry_price) / entry_price
                    self.balance *= (1 + pnl)
                    self.trades.append({
                        'type': 'sell',
                        'price': exit_price,
                        'time': timestamp,
                        'balance': self.balance,
                        'pnl': pnl
                    })
                    print(f"Sell at {exit_price} on {timestamp}. PnL: {pnl:.2%}. Balance: {self.balance:.2f}")
                    
                # Check Take Profit
                elif current_price >= entry_price * (1 + config.TAKE_PROFIT_PCT):
                     position = None
                     exit_price = current_price
                     pnl = (exit_price - entry_price) / entry_price
                     self.balance *= (1 + pnl)
                     self.trades.append({
                        'type': 'take_profit',
                        'price': exit_price,
                        'time': timestamp,
                        'balance': self.balance,
                        'pnl': pnl
                    })
                     print(f"Take Profit triggered at {exit_price} on {timestamp}. PnL: {pnl:.2%}. Balance: {self.balance:.2f}")

                # Check Stop Loss
                elif current_price <= entry_price * (1 - config.STOP_LOSS_PCT):
                     position = None
                     exit_price = current_price
                     pnl = (exit_price - entry_price) / entry_price
                     self.balance *= (1 + pnl)
                     self.trades.append({
                        'type': 'stop_loss',
                        'price': exit_price,
                        'time': timestamp,
                        'balance': self.balance,
                        'pnl': pnl
                    })
                     print(f"Stop Loss triggered at {exit_price} on {timestamp}. PnL: {pnl:.2%}. Balance: {self.balance:.2f}")

        print(f"Backtest finished. Final Balance: {self.balance:.2f}")
        return self.trades
