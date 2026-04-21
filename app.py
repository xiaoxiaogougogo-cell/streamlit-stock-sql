import os
import streamlit as st
#st.write(os listdir())
st.title("My Stock Dashboard")

st.write("App is running...")


import pandas as pd


from datetime import datetime
st.write("Last refresh:", datetime.now())

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=10000)










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



st.write("### Latest Signals")



st.dataframe(df.tail(20))




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

if st.button("Test API"):



    st.write(fetch_live_price("AAPL"))


#while True:



    #live = fetch_live_price(ticker)











     
    #live = fetch_live_price(ticker)
    
    
    #if live is None:
     #   print(f"Skipping {ticker}")

    #price = safe_get_price(ticker)
    
    
    
    if price is None:
        
        st.metric(label=ticker, value="N/A", delta="No data")
        
    else:
        st.metric(label=ticker, value=price)





    live = price

        
    
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









#paper trading
import streamlit as st



import time



import pandas as pd



from db import get_connection, init_trades_table



from live_prices import fetch_live_price



from live_signals import compute_live_signal



from paper_trading import PaperTrader



st.title("💰 Paper Trading System (Live)")







#multi-ticker issues

if "ticker" not in st.session_state:



    st.session_state.ticker = "AAPL"



ticker = st.text_input(



    "Ticker",



    st.session_state.ticker,



    key="main_ticker"



)



st.session_state.ticker = ticker














mode = st.sidebar.selectbox("Mode", ["Live", "Backtest", "Paper"])



if mode == "Live":



    import live



    live.run()



elif mode == "Backtest":



    import backtest



    backtest.run()
#######################################















ticker = st.text_input("Ticker", "AAPL")



conn = get_connection()



init_trades_table(conn)



trader = PaperTrader(10000)



trade_log = st.empty()



chart = st.empty()



metrics = st.empty()







live = fetch_live_price(ticker)



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



trades_df = pd.read_sql("SELECT * FROM trades", conn)



trade_log.write("### Trade History")



trade_log.dataframe(trades_df.tail(10))



chart.line_chart(df.set_index("time")["price"])



time.sleep(5)

st.dataframe(df)







#multi-stock portfolio treading
import streamlit as st



import time



import pandas as pd



from db import get_connection, init_portfolio_table



from live_prices import fetch_live_price



from live_signals import compute_live_signal



from paper_trading import MultiPaperTrader



st.title("📊 Multi-Stock Portfolio Trading System")



tickers = st.text_input("Tickers (comma separated)", "AAPL,MSFT,TSLA").split(",")



tickers = [t.strip().upper() for t in tickers]



conn = get_connection()



init_portfolio_table(conn)



trader = MultiPaperTrader(10000)



price_box = st.empty()



portfolio_box = st.empty()



trade_box = st.empty()



price_map = {}



while True:



    # -----------------------



    # FETCH ALL PRICES



    # -----------------------



    for t in tickers:



        live = fetch_live_price(t)



        price_map[t] = live["price"]



    # -----------------------



    # PROCESS EACH STOCK



    # -----------------------



    for t in tickers:



        df = pd.read_sql(



            "SELECT * FROM live_prices WHERE ticker = ?",



            conn,



            params=(t,)



        )



        if len(df) < 20:



            continue



        df["price"] = pd.to_numeric(df["price"])



        ma = df["price"].rolling(10).mean().iloc[-1]



        ema = df["price"].ewm(span=10).mean().iloc[-1]



        price = price_map[t]



        signal = compute_live_signal(price, ma, ema, 50)



        # -----------------------



        # EXECUTION



        # -----------------------



        if signal == "BUY":



            trader.buy(t, price)



        elif signal == "SELL":



            profit = trader.sell(t, price)



    # -----------------------



    # PORTFOLIO VALUE



    # -----------------------



    portfolio_value = trader.portfolio_value(price_map)

    risk_status = trader.update_drawdown()
    if risk_status == "KILL_SWITCH":
        st.error("🚨 KILL SWITCH ACTIVATED - TRADING STOPPED")

    risk_event = trader.check_risk(t, price)
    
    if risk_event == "STOP_LOSS":
        pnl = trader.sell(t, price, reason="STOP_LOSS")
        st.warning(f"🛑 STOP LOSS triggered on {t}")
        
    elif risk_event == "TAKE_PROFIT":
        pnl = trader.sell(t, price, reason="TAKE_PROFIT")
        st.success(f"🎯 TAKE PROFIT triggered on {t}")




    # -----------------------



    # UI



    # -----------------------



    price_box.write("### Live Prices")



    price_box.write(price_map)



    portfolio_box.metric("Portfolio Value", round(portfolio_value, 2))



    portfolio_box.metric("Cash", round(trader.capital, 2))



    portfolio_box.write("### Positions")



    portfolio_box.write(trader.positions)



    time.sleep(5)




st.write("### 🧠 Risk Dashboard")



st.metric("Capital", round(trader.capital, 2))



st.metric("Equity Peak", round(trader.equity_peak, 2))



if trader.equity_peak > 0:



    drawdown = (trader.equity_peak - trader.capital) / trader.equity_peak



    st.metric("Drawdown", f"{drawdown*100:.2f}%")



st.write("### Active Positions")



st.write(trader.positions)



if not trader.trading_enabled:



    st.error("TRADING DISABLED (Risk Limit Hit)")





#ml-model
from ml_model import train_model, predict_signal



#Train model dynamically (per ticker)



if len(df) > 50:



    model = train_model(df)



    latest = df.iloc[-1][["price", "price", "price", "price"]].values



    ml_signal = predict_signal(model, latest)



#weighting
from optimizer import compute_returns, optimize_weights



#Compute live weights:



returns = compute_returns(df)



weights = optimize_weights(returns)




#Apply weights in trading:



allocation = trader.capital * weights.get(t, 0.2)






#walk-forward testing
from broker import PaperBroker



from execution import execute_signal



#Initialize broker:



broker = PaperBroker(10000)



result = execute_signal(broker, signal, t, price)


st.write("### 💰 Portfolio Status")



st.metric("Cash", broker.get_cash())



st.write("Positions")



st.write(broker.get_positions())






#Alpaca API
from broker_factory import get_broker



#Select mode in UI:



mode = st.selectbox("Trading Mode", ["paper", "live (sandbox)"])



broker = get_broker(mode)




#🚦 7. Execution layer (same for both systems)



def execute_trade(broker, signal, ticker):



    qty = 1  # start small ALWAYS



    if signal == "BUY":



        return broker.buy(ticker, qty)



    elif signal == "SELL":



        return broker.sell(ticker, qty)



    return None


if mode == "live (sandbox)":



    st.warning("⚠️ Sandbox mode active (no real money)")



if mode == "live" and not confirm_user:



    st.error("Real trading disabled unless confirmed")



    st.stop()









#AI
st.title("🧠 Trading System Control Center")



st.metric("System Status", "ACTIVE" if state.trading_enabled else "HALTED")



st.metric("Strategy Mode", state.mode)



st.metric("Current Drawdown", drawdown)



st.metric("Win Rate", metrics.win_rate())








#db insert
