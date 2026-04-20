import streamlit as st



import pandas as pd



from db import get_connection



from backtest import backtest_strategy



from metrics import sharpe_ratio, max_drawdown, win_rate



st.title("📊 Strategy Backtesting Engine")



conn = get_connection()



df = pd.read_sql("SELECT * FROM live_prices", conn)



df["time"] = pd.to_datetime(df["time"])



if len(df) < 50:



    st.warning("Not enough data for backtest")



    st.stop()



equity, trades = backtest_strategy(df)



# -----------------------



# METRICS



# -----------------------



returns = pd.Series(equity).pct_change().dropna()



st.metric("Sharpe Ratio", round(sharpe_ratio(returns), 2))



st.metric("Max Drawdown", f"{max_drawdown(equity)*100:.2f}%")



st.metric("Win Rate", f"{win_rate(trades)*100:.2f}%")



# -----------------------



# EQUITY CURVE



# -----------------------



st.write("### Equity Curve")



st.line_chart(equity)



# -----------------------



# TRADES



# -----------------------



st.write("### Trades")



st.write(trades)
