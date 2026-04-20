import numpy as np



def sharpe(equity):



    returns = np.diff(equity) / equity[:-1]



    return np.mean(returns) / (np.std(returns) + 1e-9)



def stability_score(equity):



    # measures how consistent growth is



    peaks = max(equity)



    trough = min(equity)



    return (peaks - trough) / peaks



def overfitting_score(train_perf, test_perf):



    return train_perf - test_perf

