from alpaca.data.live import StockDataStream

API_KEY = "YOUR_KEY"
SECRET = "YOUR_SECRET"

stream = StockDataStream(API_KEY, SECRET)

def handle(data):
    print(data.symbol, data.price)

stream.subscribe_trades(handle, "AAPL")

stream.run()
