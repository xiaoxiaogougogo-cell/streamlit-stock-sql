def generate_signal(df):
    """
    Simple example strategy (replace later with RSI/MACD/ML)
    """
    if df['close'].iloc[-1] > df['ma_20'].iloc[-1]:
        return "BUY"
    elif df['close'].iloc[-1] < df['ma_20'].iloc[-1]:
        return "SELL"
    else:
        return "HOLD"
