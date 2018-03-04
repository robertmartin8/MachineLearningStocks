import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from collections import Counter


def status_calc(stock, sp500, outperformance=10):
    """A simple function to classify whether a stock outperformed the S&P500
    :param stock: stock price
    :param sp500: S&P500 price
    :param outperformance: stock is classified 1 if stock price > S&P500 price + outperformance
    :return: true/false
    """
    if outperformance < 0:
        raise ValueError("outperformance must be positive")
    return stock - sp500 >= outperformance


def build_data_set():
    """
    Reads the keystats.csv file and prepares it for scikit-learn

    :return: X_train and y_train numpy arrays
    """

    training_data = pd.read_csv("keystats.csv", index_col='Date')
    features = training_data.columns[6:]

    X_train = training_data[features].values
    y_train = list(map(
        status_calc, training_data["stock_p_change"], training_data["sp500_p_change"]))

    return X_train, y_train


def predict_stocks():
    X_train, y_train = build_data_set()
    # Remove the random_state parameter to generate actual predictions
    clf = RandomForestClassifier(n_estimators=100, random_state=0)
    clf.fit(X_train, y_train)

    # Now we get the actual data from which we want to generate predictions.
    data = pd.read_csv('forward_sample.csv', index_col='Date')
    features = data.columns[6:]
    X_test = data[features].values
    z = data["Ticker"].values

    # Get the predicted tickers
    y_pred = clf.predict(X_test)
    invest_list = z[y_pred].tolist()

    return invest_list


if __name__ == '__main__':
    predict_stocks()
