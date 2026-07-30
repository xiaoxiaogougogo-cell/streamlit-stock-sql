import yfinance as yf

def get_multi_assets(symbols):
    data = {}

    for s in symbols:
        df = yf.download(s, period="1mo", interval="5m")
        data[s] = df

    return data
