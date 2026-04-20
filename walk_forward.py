import pandas as pd



from sklearn.ensemble import RandomForestClassifier



def create_features(df):



    df = df.copy()



    df["return"] = df["price"].pct_change()



    df["ma"] = df["price"].rolling(5).mean()



    df["ema"] = df["price"].ewm(span=5).mean()



    df["target"] = (df["price"].shift(-1) > df["price"]).astype(int)



    df = df.dropna()



    X = df[["price", "ma", "ema", "return"]]



    y = df["target"]



    return X, y



def walk_forward_test(df, train_size=200, test_size=50):



    df = df.sort_values("time")



    results = []



    equity = 10000



    i = train_size



    while i + test_size < len(df):



        train = df.iloc[i-train_size:i]



        test = df.iloc[i:i+test_size]



        X_train, y_train = create_features(train)



        X_test, y_test = create_features(test)



        model = RandomForestClassifier(n_estimators=100)



        model.fit(X_train, y_train)



        predictions = model.predict(X_test)



        position = 0



        entry = 0



        for j in range(len(test)):



            price = test["price"].iloc[j]



            if predictions[j] == 1 and position == 0:



                position = equity / price



                entry = price



            elif predictions[j] == 0 and position > 0:



                equity = position * price



                position = 0



        results.append(equity)



        i += test_size



    return results


