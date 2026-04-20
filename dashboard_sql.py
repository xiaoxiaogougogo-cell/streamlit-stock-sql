import sqlite3
import streamlit
import openpyxl

import pandas as pd

df = pd.read_excel("C:/Users/Lenovo/Desktop/watchdog/stock project/db/data.xlsx")


DB_PATH = "data.db"

def get_connection():



    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():



    conn = get_connection()



    cursor = conn.cursor()



    cursor.execute("""



        CREATE TABLE IF NOT EXISTS stocks (



            date TEXT,



            ticker TEXT,



            price REAL,



            volume INTEGER



        )



    """)



    conn.commit()



    conn.close()




def insert_data(df):



    conn = get_connection()



    df.to_sql("stocks", conn, if_exists="append", index=False)



    conn.close()



def load_data():



    conn = get_connection()



    df = pd.read_sql("SELECT * FROM stocks", conn)



    conn.close()



    return df




import pandas as pd



from db import init_db, insert_data



init_db()



df = pd.read_excel("data.xlsx")

df.columns = df.columns.str.lower()



insert_data(df)



print("Data imported into SQLite successfully 👍")

import streamlit as st



from db import load_data, init_db



init_db()
st.title("📊 Trading Dashboard (SQLite Powered)")



df = load_data()



st.write("### Raw Data")
