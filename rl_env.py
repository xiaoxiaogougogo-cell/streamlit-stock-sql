import numpy as np



class TradingEnv:



    def __init__(self, prices):



        self.prices = prices



        self.index = 0



        self.balance = 10000



        self.position = 0



        self.entry_price = 0



    def reset(self):



        self.index = 0



        self.balance = 10000



        self.position = 0



        self.entry_price = 0



        return self._get_state()



    def _get_state(self):



        return np.array([



            self.prices[self.index]



        ])



    def step(self, action):



        """



        action:



        0 = HOLD



        1 = BUY



        2 = SELL



        """



        price = self.prices[self.index]



        reward = 0



        # BUY



        if action == 1 and self.position == 0:



            self.position = self.balance / price



            self.entry_price = price



        # SELL



        elif action == 2 and self.position > 0:



            reward = (price - self.entry_price) * self.position



            self.balance += reward



            self.position = 0



        self.index += 1



        done = self.index >= len(self.prices) - 1



        return self._get_state(), reward, done

