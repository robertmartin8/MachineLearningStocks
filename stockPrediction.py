import numpy as np
from sklearn import svm, preprocessing
import pandas as pd
from collections import Counter

# How much a stock has to outperform the S&P500 to be considered a success.
# Increase this value if you want fewer, but supposedly higher quality, predictions.
how_much_better = 10

FEATURES = ['DE Ratio',
            'Trailing P/E',
            'Price/Sales',
            'Price/Book',
            'Profit Margin',
            'Operating Margin',
            'Return on Assets',
            'Return on Equity',
            'Revenue Per Share',
            'Market Cap',
            'Enterprise Value',
            'Forward P/E',
            'PEG Ratio',
            'Enterprise Value/Revenue',
            'Enterprise Value/EBITDA',
            'Revenue',
            'Gross Profit',
            'EBITDA',
            'Net Income Avl to Common ',
            'Diluted EPS',
            'Earnings Growth',
            'Revenue Growth',
            'Total Cash',
            'Total Cash Per Share',
            'Total Debt',
            'Current Ratio',
            'Book Value Per Share',
            'Cash Flow',
            'Beta',
            'Held by Insiders',
            'Held by Institutions',
            'Shares Short (as of',
            'Short Ratio',
            'Short % of Float',
            'Shares Short (prior ']


def status_calc(stock, sp500):
    return stock - sp500 > how_much_better


def build_data_set():
    training_data = pd.DataFrame.from_csv("key_stats_NO_NA_enhanced.csv")

    # Randomly reorder the data, and replace NA.
    training_data = training_data.reindex(np.random.permutation(training_data.index))
    training_data = training_data.replace("NaN", 0).replace("N/A", 0)

    # Write out whether a stock has outperformed or not
    training_data["Status2"] = list(map(status_calc, training_data["stock_p_change"], training_data["sp500_p_change"]))

    # Feature scaling
    X_train = preprocessing.scale(np.array(training_data[FEATURES].values))

    y_train = training_data["Status2"] \
        .replace("underperform", 0) \
        .replace("outperform", 1) \
        .values.tolist()

    return X_train, y_train


def analysis():
    # Fit the SVC (exclude the last column).
    X_train, y_train = build_data_set()
    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(X_train[:-1], y_train[:-1])

    # Now we get the actual data from which we want to generate predictions.
    data = pd.DataFrame.from_csv("forward_sample_NO_NA.csv")
    data = data.replace("N/A", 0).replace("NaN", 0)

    X_test = preprocessing.scale(np.array(data[FEATURES].values))
    Z = data["Ticker"].values.tolist()
    invest_list = []

    # If our SVM predicts outperformance, append that stock to an invest_list.
    for i in range(len(X_test)):
        p = clf.predict(X_test[i])[0]
        if p:
            invest_list.append(Z[i])

    return invest_list

# Run the analysis multiple times (in this case, eight), and print the results
# which have turned up more than 2/3 of the time.  This code is very inelegant.

final_list = []
loops = 8

while loops:
    stock_list = analysis()
    for e in stock_list:
        final_list.append(e)
    loops -= 1

x = Counter(final_list)

print(30 * "_")
for each_prediction in x:
    # If the stock was predicted 2/3 of the time, append it.
    if x[each_prediction] > loops - (loops / 3):
        print(each_prediction)
