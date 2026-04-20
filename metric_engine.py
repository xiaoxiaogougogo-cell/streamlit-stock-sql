class Metrics:



    def __init__(self):



        self.trades = 0



        self.wins = 0



        self.losses = 0



    def log_trade(self, pnl):



        self.trades += 1



        if pnl > 0:



            self.wins += 1



        else:



            self.losses += 1



    def win_rate(self):



        if self.trades == 0:



            return 0



        return self.wins / self.trades


class Metrics:



    def __init__(self):



        self.trades = 0



        self.wins = 0



        self.losses = 0



    def log_trade(self, pnl):



        self.trades += 1



        if pnl > 0:



            self.wins += 1



        else:



            self.losses += 1



    def win_rate(self):



        if self.trades == 0:



            return 0



        return self.wins / self.trades


def detect_anomaly(price_series):



    if len(price_series) < 10:



        return False



    volatility = price_series.pct_change().std()



    if volatility > 0.05:



        return True  # market unstable



    return False

#add alert system
def alert(message):



    print("🚨 ALERT:", message)
