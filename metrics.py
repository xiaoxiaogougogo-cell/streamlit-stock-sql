import numpy as np



def sharpe_ratio(returns):



    returns = np.array(returns)



    return np.mean(returns) / (np.std(returns) + 1e-9)



def max_drawdown(equity):



    peak = equity[0]



    max_dd = 0



    for x in equity:



        peak = max(peak, x)



        dd = (peak - x) / peak



        max_dd = max(max_dd, dd)



    return max_dd



def win_rate(trades):



    wins = 0



    total = 0



    for t in trades:



        if len(t) == 3:



            total += 1



            if t[2] > 0:



                wins += 1



    return wins / total if total > 0 else 0
