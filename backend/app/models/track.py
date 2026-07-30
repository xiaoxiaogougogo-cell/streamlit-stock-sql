import pandas as pd

class Portfolio:
    def __init__(self):
        self.trades = []

    def add_trade(self, symbol, side, price, qty):
        self.trades.append({
            "symbol": symbol,
            "side": side,
            "price": price,
            "qty": qty
        })

    def to_df(self):
        return pd.DataFrame(self.trades)
