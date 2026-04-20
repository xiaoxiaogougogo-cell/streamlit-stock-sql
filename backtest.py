import pandas as pd



import numpy as np



def backtest_strategy(df):



    df = df.copy()



    df = df.sort_values("time")



    df["return"] = df["price"].pct_change()



    capital = 10000



    position = 0



    entry_price = 0



    equity_curve = []



    trades = []



    for i in range(20, len(df)):



        price = df["price"].iloc[i]



        ma = df["price"].iloc[i-10:i].mean()



        ema = df["price"].iloc[i-10:i].ewm(span=10).mean().iloc[-1]



        rsi = 50  # simplified for backtest



        signal = "HOLD"



        if ma > ema:



            signal = "BUY"



        elif ma < ema:



            signal = "SELL"



        # -----------------------



        # EXECUTION



        # -----------------------



        if signal == "BUY" and position == 0:



            position = capital / price



            entry_price = price



            trades.append(("BUY", price))



        elif signal == "SELL" and position > 0:



            capital = position * price



            pnl = (price - entry_price) * position



            position = 0



            trades.append(("SELL", price, pnl))



        # -----------------------



        # equity update



        # -----------------------



        equity = capital if position == 0 else position * price



        equity_curve.append(equity)



    return equity_curve, trades
