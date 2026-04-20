
def generate_signals(df):



    df = df.copy()



    df["signal"] = "HOLD"



    if "MA_20" in df.columns and "EMA_20" in df.columns:



        df.loc[df["MA_20"] > df["EMA_20"], "signal"] = "BUY"



        df.loc[df["MA_20"] < df["EMA_20"], "signal"] = "SELL"



    # RSI filter (optional refinement)



    if "RSI" in df.columns:



        df.loc[df["RSI"] > 70, "signal"] = "SELL"



        df.loc[df["RSI"] < 30, "signal"] = "BUY"



    return df

