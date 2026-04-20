import datetime



def log_event(event_type, message):



    print(f"[{datetime.datetime.now()}] {event_type}: {message}")



#performance tracking


class PerformanceTracker:



    def __init__(self):



        self.pnl = []



        self.equity = 10000



    def update(self, pnl):



        self.equity += pnl



        self.pnl.append(self.equity)



    def sharpe(self):



        import numpy as np



        returns = np.diff(self.pnl) / np.array(self.pnl[:-1])



        return np.mean(returns) / (np.std(returns) + 1e-9)






#🛑 4. Add system resilience layer (VERY IMPORTANT in production)

class CircuitBreaker:



    def __init__(self):



        self.failures = 0



        self.max_failures = 5



        self.active = True



    def record_failure(self):



        self.failures += 1



        if self.failures >= self.max_failures:



            self.active = False



    def allow_trade(self):



        return self.active
