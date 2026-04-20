def execute_signal(broker, signal, ticker, price):



    qty = 10  # fixed size or later risk-based



    if signal == "BUY":



        return broker.buy(ticker, qty, price)



    elif signal == "SELL":



        return broker.sell(ticker, qty, price)



    return "HOLD"
