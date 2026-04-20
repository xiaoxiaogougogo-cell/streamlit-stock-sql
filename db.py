import sqlite3



import pandas as pd



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



def insert_live_price(conn, ticker, price, time):



    cursor = conn.cursor()



    cursor.execute("""



        CREATE TABLE IF NOT EXISTS live_prices (



            time TEXT,



            ticker TEXT,



            price REAL



        )



    """)



    cursor.execute("""



        INSERT INTO live_prices (time, ticker, price)



        VALUES (?, ?, ?)



    """, (time, ticker, price))



    conn.commit()



#paper trading
def init_trades_table(conn):



    cursor = conn.cursor()



    cursor.execute("""



        CREATE TABLE IF NOT EXISTS trades (



            time TEXT,



            ticker TEXT,



            action TEXT,



            price REAL,



            profit REAL



        )



    """)



    conn.commit()





#multi-stock portfoliio trading
def init_portfolio_table(conn):



    cursor = conn.cursor()



    cursor.execute("""



        CREATE TABLE IF NOT EXISTS portfolio (



            ticker TEXT,



            position REAL,



            avg_price REAL,



            last_price REAL,



            pnl REAL



        )



    """)



    conn.commit()



    #Alpaca API 

    
def log_trade(conn, ticker, action, price):



    cursor = conn.cursor()



    cursor.execute("""



        CREATE TABLE IF NOT EXISTS trades (



            time TEXT,



            ticker TEXT,



            action TEXT,



            price REAL



        )



    """)



    import datetime



    cursor.execute("""



        INSERT INTO trades VALUES (?, ?, ?, ?)



    """, (



        str(datetime.datetime.now()),



        ticker,



        action,



        price



    ))



    conn.commit()



