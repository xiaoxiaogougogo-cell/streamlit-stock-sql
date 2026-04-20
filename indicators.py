import pandas as pd



# -------------------------



# Moving Average



# -------------------------



def add_ma(df, window=20):



    df = df.copy()



    df[f"MA_{window}"] = df["price"].rolling(window=window).mean()



    return df



# -------------------------



# Exponential Moving Average



# -------------------------



def add_ema(df, window=20):



    df = df.copy()



    df[f"EMA_{window}"] = df["price"].ewm(span=window, adjust=False).mean()



    return df



# -------------------------



# RSI (Relative Strength Index)



# -------------------------



def add_rsi(df, window=14):



    df = df.copy()



    delta = df["price"].diff()



    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()



    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()



    rs = gain / loss



    df["RSI"] = 100 - (100 / (1 + rs))



    return df





#live_price
def calculate_indicators(df):



    df = df.copy()



    df["MA_10"] = df["price"].rolling(10).mean()



    df["EMA_10"] = df["price"].ewm(span=10).mean()



    # RSI



    delta = df["price"].diff()



    gain = delta.clip(lower=0).rolling(14).mean()



    loss = (-delta.clip(upper=0)).rolling(14).mean()



    rs = gain / loss



    df["RSI"] = 100 - (100 / (1 + rs))



    return df



