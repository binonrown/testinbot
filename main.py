import argparse
import pandas as pd
from bot.trader import Trader
from backtester.engine import Backtester
import config

def main():
    parser = argparse.ArgumentParser(description="Binance Trading Bot 'binonrown'")
    parser.add_argument('--mode', choices=['live', 'backtest'], default='live', help='Mode to run the bot in')
    parser.add_argument('--testnet', action='store_true', help='Use Binance Testnet')
    args = parser.parse_args()

    if args.mode == 'live':
        trader = Trader(testnet=args.testnet)
        trader.run()
    
    elif args.mode == 'backtest':
        # For backtesting, we need data. 
        # In a real scenario, we'd fetch historical data or load from CSV.
        # Here we will fetch some recent data using the Trader class for demonstration.
        print("Fetching data for backtest...")
        trader = Trader()
        df = trader.fetch_data(config.SYMBOL, config.TIMEFRAME, limit=500)
        
        backtester = Backtester(initial_balance=config.INITIAL_BALANCE)
        backtester.run(df)

if __name__ == "__main__":
    main()
