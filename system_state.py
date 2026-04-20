class SystemState:



    def __init__(self):



        self.trading_enabled = True



        self.mode = "paper"



        self.last_error = None



    def halt(self, reason):



        self.trading_enabled = False



        self.last_error = reason



    def resume(self):



        self.trading_enabled = True



        self.last_error = None


