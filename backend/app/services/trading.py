mport time
from engine.strategy import generate_signal
from broker.alpaca_paper import buy
from alerts.telegram import send

symbol = "AAPL"

while True:
    price = 180  # replace with live feed
    ma_fast = 181
    ma_slow = 179

    signal = generate_signal(price, ma_fast, ma_slow)

    if signal == "BUY":
        buy(symbol, 1)
        send(f"BUY {symbol}")

    elif signal == "SELL":
        send(f"SELL {symbol}")

    time.sleep(60)
root@ubuntu-s-1vcpu-1
