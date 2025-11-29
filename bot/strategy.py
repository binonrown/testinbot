import pandas as pd

class Strategy:
    def __init__(self):
        pass

    def calculate_rsi(self, data, window=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signal(self, df):
        # Strategy: SMA Crossover + RSI Filter
        # Buy: SMA 20 > SMA 50 AND RSI < 70 (Not overbought)
        # Sell: SMA 20 < SMA 50
        
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        df['RSI'] = self.calculate_rsi(df['close'])
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        # Ensure we have enough data
        if pd.isna(last_row['SMA_50']) or pd.isna(prev_row['SMA_50']) or pd.isna(last_row['RSI']):
            return None
        
        # Buy Signal
        if (prev_row['SMA_20'] <= prev_row['SMA_50'] and 
            last_row['SMA_20'] > last_row['SMA_50'] and 
            last_row['RSI'] < 70):
            return 'buy'
            
        # Sell Signal
        elif prev_row['SMA_20'] >= prev_row['SMA_50'] and last_row['SMA_20'] < last_row['SMA_50']:
            return 'sell'
        
        return None
