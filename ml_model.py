import pandas as pd



from sklearn.ensemble import RandomForestClassifier



def prepare_data(df):



    df = df.copy()



    df["return"] = df["price"].pct_change()



    df["ma"] = df["price"].rolling(5).mean()



    df["ema"] = df["price"].ewm(span=5).mean()



    df["target"] = (df["price"].shift(-1) > df["price"]).astype(int)



    df = df.dropna()



    features = df[["price", "ma", "ema", "return"]]



    target = df["target"]



    return features, target



def train_model(df):



    X, y = prepare_data(df)



    model = RandomForestClassifier(n_estimators=100)



    model.fit(X, y)



    return model



def predict_signal(model, latest_row):



    pred = model.predict([latest_row])[0]



    return "BUY" if pred == 1 else "SELL"

