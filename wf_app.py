import streamlit as st



import pandas as pd



from db import get_connection



from walk_forward import walk_forward_test



from validation_metrics import sharpe



st.title("🧠 Walk-Forward ML Validation System")



conn = get_connection()



df = pd.read_sql("SELECT * FROM live_prices", conn)



df["time"] = pd.to_datetime(df["time"])



if len(df) < 300:



    st.warning("Need more data for walk-forward test")



    st.stop()

results = walk_forward_test(df)



# -----------------------



# METRICS



# -----------------------



st.metric("Final Equity", round(results[-1], 2))



st.metric("Sharpe Ratio", round(sharpe(results), 2))



# -----------------------



# EQUITY CURVE



# -----------------------



st.write("### Walk-Forward Equity Curve")



st.line_chart(results)

