import numpy as np



import pandas as pd



def compute_returns(df):



    returns = df.pivot(index="time", columns="ticker", values="price").pct_change()



    return returns



def sharpe_ratio(series):



    return np.mean(series) / np.std(series)



def optimize_weights(returns):



    scores = {}



    for col in returns.columns:



        scores[col] = sharpe_ratio(returns[col].dropna())



    total = sum(abs(v) for v in scores.values())



    weights = {k: v / total for k, v in scores.items()}



    return weights
