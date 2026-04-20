import yfinance as yf



import pandas as pd



def get_sp500(start="2023-01-01"):



    sp = yf.download("^GSPC", start=start)



    sp = sp.reset_index()



    sp = sp[["Date", "Close"]]



    sp.columns = ["date", "sp500"]



    return sp




def normalize(df, col):



    df = df.copy()



    df[col] = (df[col] / df[col].iloc[0]) * 100



    return df


