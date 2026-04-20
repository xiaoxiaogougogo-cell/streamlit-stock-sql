from broker import PaperBroker



from alpaca_broker import AlpacaBroker



def get_broker(mode="paper"):



    if mode == "paper":



        return PaperBroker(10000)



    elif mode == "live":



        return AlpacaBroker(



            api_key="YOUR_KEY",



            secret_key="YOUR_SECRET",



            paper=True  # change to False for real money



        )

