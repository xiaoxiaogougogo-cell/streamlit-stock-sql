from alpaca.trading.client import TradingClient



from alpaca.trading.requests import MarketOrderRequest



from alpaca.trading.enums import OrderSide, TimeInForce



class AlpacaBroker:



    def __init__(self, api_key, secret_key, paper=True):



        self.client = TradingClient(



            api_key,



            secret_key,



            paper=paper



        )



    def buy(self, ticker, qty):



        order = MarketOrderRequest(



            symbol=ticker,



            qty=qty,



            side=OrderSide.BUY,



            time_in_force=TimeInForce.DAY



        )



        return self.client.submit_order(order)



    def sell(self, ticker, qty):



        order = MarketOrderRequest(



            symbol=ticker,



            qty=qty,



            side=OrderSide.SELL,



            time_in_force=TimeInForce.DAY



        )



        return self.client.submit_order(order)



    def get_positions(self):



        return self.client.get_all_positions()



    def get_account(self):



        return self.client.get_account()

