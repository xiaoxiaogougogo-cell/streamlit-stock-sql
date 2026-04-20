import yfinance as yf



import pandas as pd



from datetime import datetime



#def fetch_live_price(ticker):



#    data = yf.Ticker(ticker)



#    price = data.history(period="1d", interval="1m").tail(1)["Close"].iloc[0]



#    return {



#        "ticker": ticker,



#        "price": float(price),



#        "time": datetime.now()



#    }










def fetch_live_price(ticker):



    try:



        data = yf.Ticker(ticker)

        price = data.history(period="1d", interval="1m")



        #price = data.history(period="1d", interval="1m")



        # 🚨 Check 1: None or empty



        if price is None or price.empty:



            print(f"No data for {ticker}")



            return None



        # 🚨 Check 2: column exists



        if "Close" not in price.columns:



            print(f"'Close' column missing for {ticker}")



            return None



        price = price["Close"].iloc[-1]

       #return price

        return {



        "ticker": ticker,



        "price": float(price),



        "time": datetime.now()



    }




        
    



    except Exception as e:



        print(f"Error fetching {ticker}: {e}")



        return None








import logging



logging.basicConfig(filename="app.log", level=logging.ERROR)




def safe_get_price(ticker):



    data = fetch_live_price(ticker)



    if data is None:



        return None



    if "price" not in data:



        return None



    return data["price"]









