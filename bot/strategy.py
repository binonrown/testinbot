import pandas as pd

class Strategy:
    def __init__(self):
        pass

    def generate_signal(self, df):
        # Example Strategy: SMA Crossover
        # Buy when SMA 20 crosses above SMA 50
        # Sell when SMA 20 crosses below SMA 50
        
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        # Ensure we have enough data
        if pd.isna(last_row['SMA_50']) or pd.isna(prev_row['SMA_50']):
            return None
        
        if prev_row['SMA_20'] <= prev_row['SMA_50'] and last_row['SMA_20'] > last_row['SMA_50']:
            return 'buy'
        elif prev_row['SMA_20'] >= prev_row['SMA_50'] and last_row['SMA_20'] < last_row['SMA_50']:
            return 'sell'
        
        return None
