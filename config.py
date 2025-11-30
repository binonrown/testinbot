import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Trading Configuration
SYMBOL = "BTC/USDT"
TIMEFRAME = "1h"
MAX_DAILY_TRADES = 10
STOP_LOSS_PCT = 0.02  # 2% stop loss
TAKE_PROFIT_PCT = 0.04 # 4% take profit

# Backtesting Configuration
INITIAL_BALANCE = 200
