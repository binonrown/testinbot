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
        # Strategy: Dip Buying (RSI + Green Candle)
        # Buy: RSI < 30 (Oversold/Low) AND Current Candle is Green (Close > Open)
        # Sell: RSI > 70 (Overbought/High)
        
        df['RSI'] = self.calculate_rsi(df['close'])
        
        last_row = df.iloc[-1]
        
        # Ensure we have enough data
        if pd.isna(last_row['RSI']):
            return None
        
        # Define Green Candle
        is_green_candle = last_row['close'] > last_row['open']
        
        # Buy Signal
        if last_row['RSI'] < 30 and is_green_candle:
            return 'buy'
            
        # Sell Signal
        elif last_row['RSI'] > 70:
            return 'sell'
        
        return None
