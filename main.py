import argparse
import pandas as pd
from bot.trader import Trader
from backtester.engine import Backtester
import config

def main():
    parser = argparse.ArgumentParser(description="Binance Trading Bot 'binonrown'")
    parser.add_argument('--mode', choices=['live', 'backtest'], default='live', help='Mode to run the bot in')
    parser.add_argument('--testnet', action='store_true', help='Use Binance Testnet')
    parser.add_argument('--duration', type=str, help='Duration to run the bot (e.g., "30m", "1h"). If not set, runs once.')
    parser.add_argument('--unlimited-trades', action='store_true', help='Disable max daily trades limit')
    args = parser.parse_args()

    if args.mode == 'live':
        max_trades = float('inf') if args.unlimited_trades else None
        trader = Trader(testnet=args.testnet, max_daily_trades=max_trades)
        
        if args.duration:
            import time
            import re
            
            # Parse duration
            match = re.match(r"(\d+)([mh])", args.duration)
            if not match:
                print("Invalid duration format. Use '30m' or '1h'.")
                return
            
            value = int(match.group(1))
            unit = match.group(2)
            seconds = value * 60 if unit == 'm' else value * 3600
            
            end_time = time.time() + seconds
            print(f"Running for {args.duration} with unlimited trades={args.unlimited_trades}...")
            
            while time.time() < end_time:
                trader.run()
                time.sleep(60) # Wait 1 minute between checks
        else:
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
