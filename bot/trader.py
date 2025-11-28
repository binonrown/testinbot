import ccxt
import pandas as pd
from .strategy import Strategy
from .risk_manager import RiskManager
import config

class Trader:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': config.BINANCE_API_KEY,
            'secret': config.BINANCE_SECRET_KEY,
            'enableRateLimit': True,
        })
        # Use sandbox for testing if needed, but for now assuming live or testnet keys provided
        # self.exchange.set_sandbox_mode(True) 
        
        self.strategy = Strategy()
        self.risk_manager = RiskManager(config.MAX_DAILY_TRADES, config.STOP_LOSS_PCT)

    def fetch_data(self, symbol, timeframe, limit=100):
        bars = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def execute_trade(self, symbol, side, amount):
        if not self.risk_manager.check_trade_allowed():
            print("Max daily trades reached. Trade skipped.")
            return

        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            print(f"Executed {side} order for {symbol}: {order}")
            self.risk_manager.record_trade()
            
            # Place Stop Loss (simplified, ideally should be OCO or separate order logic)
            # This is a placeholder for actual execution logic which can be complex
            entry_price = order['price'] # Assuming market order returns price immediately or fetch it
            stop_loss_price = self.risk_manager.calculate_stop_loss(entry_price, side)
            print(f"Stop loss calculated at: {stop_loss_price}")
            
        except Exception as e:
            print(f"Trade failed: {e}")

    def run(self):
        print(f"Starting bot for {config.SYMBOL}...")
        df = self.fetch_data(config.SYMBOL, config.TIMEFRAME)
        signal = self.strategy.generate_signal(df)
        
        if signal:
            print(f"Signal detected: {signal}")
            # Amount logic needs to be defined, using a placeholder
            amount = 0.001 
            self.execute_trade(config.SYMBOL, signal, amount)
        else:
            print("No signal detected.")
