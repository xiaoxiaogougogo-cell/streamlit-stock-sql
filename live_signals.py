def compute_live_signal(price, ma, ema, rsi):



    signal = "HOLD"



    # Trend logic



    if ma > ema:



        signal = "BUY"



    elif ma < ema:



        signal = "SELL"



    # Momentum override (strong conditions)



    if rsi > 70:



        signal = "SELL"



    elif rsi < 30:



        signal = "BUY"



    return signal


