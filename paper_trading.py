class RiskManagedTrader:



    def __init__(self, capital=10000):



        self.capital = capital



        self.positions = {}



        self.equity_peak = capital



        # risk settings



        self.stop_loss = 0.05      # 5%



        self.take_profit = 0.10    # 10%



        self.max_drawdown = 0.15   # 15% kill switch



        self.trading_enabled = True



    def buy(self, ticker, price):



        if not self.trading_enabled:



            return "TRADING HALTED"



        if ticker in self.positions:



            return "ALREADY HOLDING"



        allocation = self.capital * 0.15  # 15% risk per trade



        qty = allocation / price



        self.positions[ticker] = {



            "entry": price,



            "qty": qty



        }



        return f"BUY {ticker}"



    def sell(self, ticker, price, reason="manual"):



        if ticker not in self.positions:



            return 0



        entry = self.positions[ticker]["entry"]



        qty = self.positions[ticker]["qty"]



        pnl = (price - entry) * qty



        self.capital += pnl



        del self.positions[ticker]



        return pnl



    def check_risk(self, ticker, price):



        if ticker not in self.positions:



            return None



        entry = self.positions[ticker]["entry"]



        change = (price - entry) / entry



        # STOP LOSS



        if change <= -self.stop_loss:



            return "STOP_LOSS"



        # TAKE PROFIT



        if change >= self.take_profit:



            return "TAKE_PROFIT"



        return None



    def update_drawdown(self):



        equity = self.capital + self.unrealized_pnl()



        self.equity_peak = max(self.equity_peak, equity)



        drawdown = (self.equity_peak - equity) / self.equity_peak



        if drawdown > self.max_drawdown:



            self.trading_enabled = False



            return "KILL_SWITCH"



        return "OK"



    def unrealized_pnl(self):



        return 0  # simplified (can upgrade later)



    def portfolio_value(self, prices):



        value = self.capital



        for t, pos in self.positions.items():



            if t in prices:



                value += pos["qty"] * prices[t]



        return value



#paper trading engine
class PaperTrader:



    def __init__(self, capital=10000):



        self.capital = capital



        self.position = None  # (price, qty)



    def buy(self, price):



        if self.position is None:



            qty = self.capital / price



            self.position = (price, qty)



            return "BUY EXECUTED"



        return "ALREADY IN POSITION"



    def sell(self, price):



        if self.position is not None:



            entry_price, qty = self.position



            profit = (price - entry_price) * qty



            self.capital += profit



            self.position = None



            return profit



        return 0


