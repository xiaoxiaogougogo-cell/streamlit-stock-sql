import time



from broker_factory import get_broker



from live_prices import fetch_live_price



from live_signals import compute_live_signal



from db import get_connection



broker = get_broker("paper")  # switch later to live



conn = get_connection()



tickers = ["AAPL", "MSFT", "TSLA"]



print("🚀 Trading bot started...")



while True:



    prices = {}



    for t in tickers:



        live = fetch_live_price(t)



        price = live["price"]



        prices[t] = price



        # --- signal logic (simple)



        signal = compute_live_signal(price, price, price, 50)



        if signal == "BUY":



            broker.buy(t, 1)



        elif signal == "SELL":



            broker.sell(t, 1)
            print("Prices:", prices)


        if not state.trading_enabled:
            print("⛔ Trading halted:", state.last_error)
            continue

        




    time.sleep(10)


