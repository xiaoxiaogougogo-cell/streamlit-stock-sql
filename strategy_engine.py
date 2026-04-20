def ma_strategy(price, ma, ema):



    if ma > ema:



        return "BUY"



    elif ma < ema:



        return "SELL"



    return "HOLD"



def rsi_strategy(rsi):



    if rsi < 30:



        return "BUY"



    elif rsi > 70:



        return "SELL"



    return "HOLD"



def ml_strategy(pred):



    return "BUY" if pred == 1 else "SELL"


def combine_signals(signals):



    score = 0



    for s in signals:



        if s == "BUY":



            score += 1



        elif s == "SELL":



            score -= 1



    if score >= 2:



        return "BUY"



    elif score <= -2:



        return "SELL"



    else:



        return "HOLD"




import numpy as np



def risk_parity(returns):



    vol = returns.std()



    weights = 1 / (vol + 1e-9)



    return weights / weights.sum()





class RiskEngine:



    def __init__(self):



        self.max_drawdown = 0.2



        self.daily_loss_limit = 0.05



    def allow_trade(self, drawdown):



        if drawdown > self.max_drawdown:



            return False



        return True


