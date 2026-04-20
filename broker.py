class BrokerInterface:



    def buy(self, ticker, qty, price=None):



        raise NotImplementedError



    def sell(self, ticker, qty, price=None):



        raise NotImplementedError



    def get_positions(self):



        raise NotImplementedError



    def get_cash(self):



        raise NotImplementedError




#💰 2. Paper broker (safe trading engine)



class PaperBroker(BrokerInterface):



    def __init__(self, capital=10000):



        self.cash = capital



        self.positions = {}



    def buy(self, ticker, qty, price):



        cost = qty * price



        if cost > self.cash:



            return "INSUFFICIENT CASH"



        self.cash -= cost



        if ticker in self.positions:



            self.positions[ticker] += qty



        else:



            self.positions[ticker] = qty



        return f"BUY {ticker}"



    def sell(self, ticker, qty, price):



        if ticker not in self.positions:



            return "NO POSITION"



        self.positions[ticker] -= qty



        self.cash += qty * price



        if self.positions[ticker] <= 0:



            del self.positions[ticker]



        return f"SELL {ticker}"



    def get_positions(self):



        return self.positions



    def get_cash(self):



        return self.cash





