import os
import streamlit as st




import pandas as pd


from datetime import datetime
st.write("Last refresh:", datetime.now())

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=10000)


import streamlit as st



import time



import pandas as pd



from db import get_connection, init_trades_table

from db import get_connection, insert_live_price

from backend.app.live_prices import fetch_live_price




from live_signals import compute_live_signal



from paper_trading import PaperTrader



st.title("💰 Paper Trading System (Live)")







ticker = st.text_input("Ticker", "AAPL")



conn = get_connection()



init_trades_table(conn)



trader = PaperTrader(10000)



trade_log = st.empty()



chart = st.empty()



metrics = st.empty()



while True:



    live = fetch_live_price(ticker)



    insert_live_price(conn, live["ticker"],live["price"], str(live["time"]))



    df = pd.read_sql(



        "SELECT * FROM live_prices WHERE ticker = ?",



        conn,



        params=(ticker,)



    )





    df["time"] = pd.to_datetime(df["time"])



    df = df.dropna()



    price = live["price"]



    # -----------------------



    # Simple signal logic



    # -----------------------



    if len(df) > 20:



        ma = df["price"].rolling(10).mean().iloc[-1]



        ema = df["price"].ewm(span=10).mean().iloc[-1]



        signal = compute_live_signal(price, ma, ema, 50)



        # -----------------------



        # EXECUTION ENGINE



        # -----------------------



        if signal == "BUY":



            trader.buy(price)



        elif signal == "SELL":



            profit = trader.sell(price)



            cursor = conn.cursor()



            cursor.execute("""



                INSERT INTO trades (time, ticker, action, price, profit)



                VALUES (?, ?, ?, ?, ?)



            """, (str(live["time"]), ticker, "SELL", price, profit))



            conn.commit()



    # -----------------------



    # UI



    # -----------------------
  
  

    metrics.metric("Capital", round(trader.capital, 2))



    metrics.metric("Current Price", price)



#
    trades_df = pd.read_sql("SELECT * FROM trades", conn)

    ################
    
    #position = 0  # 0 = no position, 1 = holding

    #"position": position
#    df_trades = pd.read_csv("trades.csv")


   
    
    
    
    
   # df = trades_df[["time", "action", "price"]]
    #df_trades = pd.read_csv("trades.csv")


   


 #   st.dataframe(df_trades.tail(10))


    #trades_df.to_csv(r"C:/Users/Lenovo/Desktop/watchdog/stock project/parque/trades.csv", index=False)
    #################


 
    trade_log.write("### Trade History")



    trade_log.dataframe(trades_df.tail(10))
     
    
    
    st.write("Number of trades:", len(trades_df)) 
    
    

    st.line_chart(df.set_index("time")["price"])
#    chart.line_chart(df.set_index("time")["price"])




    time.sleep(5)


