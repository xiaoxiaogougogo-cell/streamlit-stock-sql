from helper import r

def publish_tick(ticker, price):
    return r.xadd(
    "market_ticks",
    {
        "ticker": ticker,
        "price": float(price),
        "timestamp": datetime.utcnow().isoformat()
    }
) 


 
