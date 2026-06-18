import os
import streamlit as st


#t.write(st.secrets["API_KEY"])#st.write(os listdir())


st.write("App is running...")


import pandas as pd


from datetime import datetime
st.write("Last refresh:", datetime.now())

from streamlit_autorefresh import st_autorefresh
#st_autorefresh(interval=10000)
import time

#st.write("Last trade from DB:", last_trade_time)
st.write("Time:", pd.Timestamp.now())




from db import init_db, insert_data

st.title("📊 Live Trading Dashboard (SQLite)")

init_db()
data = "C:/Users/Lenovo/Desktop/watchdog/stock project/db/data.xlsx"
df = pd.read_excel("data.xlsx")
df.to_parquet("data.parquet")



df = pd.read_parquet("data.parquet")


# optional cleaning step

df.columns = df.columns.str.lower()

#insert_data(df)

#df = load_data()

st.write("### Raw Data")
st.dataframe(df)


st.write("### Summary")

st.metric("Rows", len(df))



st.metric("Tickers", df["ticker"].nunique())




if "price" in df.columns:

    st.line_chart(df.groupby("date")["price"].mean())






from indicators import add_ma, add_ema, add_rsi

from signals import generate_signals

init_db()


st.title("📊 Trading Dashboard with Signals")


# Sort by time if available



if "date" in df.columns:



    df = df.sort_values("date")



# -----------------------



# Add indicators



# -----------------------



df = add_ma(df, 20)


df = add_ema(df, 20)


df = add_rsi(df, 14)


df = generate_signals(df)



st.write("### Latest Data")

st.dataframe(df.tail(20))

if "MA_20" in df.columns:

    st.line_chart(df[["price", "MA_20", "EMA_20"]])







#benchmark
import pandas as pd


import streamlit as st



from db import load_data, init_db



from benchmark import get_sp500



from indicators import add_ma, add_ema, add_rsi



from signals import generate_signals



init_db()



st.title("📊 Trading Dashboard vs S&P 500")



# -----------------------



# Load data



# -----------------------



df = load_data()

df = df.sort_values("date")

# Convert date format if needed

df["date"] = pd.to_datetime(df["date"])

# -----------------------



# Portfolio aggregation



# -----------------------

portfolio = df.groupby("date")["price"].mean().reset_index()


portfolio.columns = ["date", "portfolio"]


# -----------------------



# Load S&P 500



# -----------------------



sp = get_sp500(start=portfolio["date"].min())



# Merge



merged = pd.merge(portfolio, sp, on="date", how="inner")



# -----------------------



# Normalize



# -----------------------

if not merged.empty and "sp500" in merged.columns:



    first_val = merged["sp500"].dropna()

    if not first_val.empty:



        base = first_val.iloc[0]



        merged["sp500"] = merged["sp500"] / base
        merged["sp500"] = merged["sp500"] / merged["SP500"].iloc[0] *100
        merged["portfolio_norm"] = (merged["portfolio"] / merged["portfolio"].iloc[0]) * 100
        st.write("### 📈 Portfolio vs S&P 500")
        st.line_chart(merged[["portfolio_norm", "sp500_norm"]])
        portfolio_return = merged["portfolio_norm"].iloc[-1] - 100  
        sp_return = merged["sp500_norm"].iloc[-1] - 100
        alpha = portfolio_return - sp_return
        st.metric("Portfolio Return %", round(portfolio_return, 2))
        st.metric("S&P 500 Return %", round(sp_return, 2))
        st.metric("Alpha (outperformance)", round(alpha, 2))
        df = add_ma(df, 20)
        df = add_ema(df, 20)
        df = add_rsi(df, 14)
        df = generate_signals(df)
        st.write("### Latest Signals")
        st.dataframe(df.tail(20))



# -----------------------



# Signals still included



# -----------------------



df = add_ma(df, 20)



df = add_ema(df, 20)



df = add_rsi(df, 14)



df = generate_signals(df)



#st.write("### Latest Signals")



#st.dataframe(df.tail(20))




###########################3tempr
st.write(df.tail())

st.write(df.columns)










#live trading-live pricing
import streamlit as st



import time



import pandas as pd



from db import get_connection, insert_live_price



from live_prices import fetch_live_price, safe_get_price


st.title("📊 Live Trading Dashboard (Real-Time)")



ticker = st.text_input("Enter ticker", "AAPL")



placeholder = st.empty()



conn = get_connection()



# -------------------------



# LIVE LOOP



# -------------------------

#if st.button("Test API"):



 #   st.write(fetch_live_price("AAPL"))


#while True:



    #live = fetch_live_price(ticker)











     

    
    
    #if live is None:
     #   print(f"Skipping {ticker}")

    #price = safe_get_price(ticker)
    
    
    
#if price is None:
        
#        st.metric(label=ticker, value="N/A", delta="No data")
        
#else:
 #3       st.metric(label=ticker, value=price)





#live = price

live = fetch_live_price(ticker)        
    
insert_live_price(conn, live["ticker"], live["price"], str(live["time"]))



df = pd.read_sql("SELECT * FROM live_prices WHERE ticker = ?", conn, params=(ticker,))



df["time"] = pd.to_datetime(df["time"])



with placeholder.container():



        st.metric("Live Price", df["price"].iloc[-1])



        st.write("### Price History (Live)")



        st.line_chart(df.set_index("time")["price"])



        st.write("### Last 10 updates")



        st.dataframe(df.tail(10))



time.sleep(5)








# live signal engine



# alerts
import streamlit as st



import time



import pandas as pd



from db import get_connection, insert_live_price



from live_prices import fetch_live_price


from indicators import calculate_indicators

from live_signals import compute_live_signal





st.title("🚨 Live Trading Alert System")



ticker = st.text_input("Ticker", "AAPL")



placeholder = st.empty()



alert_box = st.empty()



conn = get_connection()



#while True:



live = fetch_live_price(ticker)



insert_live_price(conn, live["ticker"], live["price"], str(live["time"]))



df = pd.read_sql(



        "SELECT * FROM live_prices WHERE ticker = ?",



        conn,



        params=(ticker,)



    )



df["time"] = pd.to_datetime(df["time"])



    # -----------------------



    # Indicators



    # -----------------------




df = calculate_indicators(df)



last = df.dropna().iloc[-1]



signal = compute_live_signal(



        price=last["price"],



        ma=last["MA_10"],



        ema=last["EMA_10"],



        rsi=last["RSI"]



    )



    # -----------------------



    # ALERT SYSTEM 🚨



    # -----------------------



if signal == "BUY":



        alert_box.success("🟢 BUY SIGNAL DETECTED")



elif signal == "SELL":



        alert_box.error("🔴 SELL SIGNAL DETECTED")



else:



        alert_box.info("⚪ HOLD")



    # -----------------------



    # UI



    # -----------------------



with placeholder.container():



        st.metric("Live Price", last["price"])



        st.metric("Signal", signal)



        st.metric("RSI", round(last["RSI"], 2))



        st.line_chart(df.set_index("time")["price"])



time.sleep(5)









































mode = st.sidebar.selectbox("Mode", ["Live", "Backtest", "Paper"])



if mode == "Live":



    import app



    live.run()




elif mode == "Backtest":



    import backtest_app



##    backtest_app.run()
elif mode == "Paper":
      import paper_trading
      paper_trading.run()
      

 
