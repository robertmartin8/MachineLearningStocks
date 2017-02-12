import numpy as np
from sklearn import svm, preprocessing
import pandas as pd
from collections import Counter

# How much a stock has to outperform the S&P500 to be considered a success.
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


def Status_Calc(stock, sp500):
    difference = stock - sp500
    if difference > how_much_better:
        return 1
    else:
        return 0


def Build_Data_Set():
    data_df = pd.DataFrame.from_csv("key_stats_NO_NA_enhanced.csv")
    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.replace("NaN", 0).replace("N/A", 0)

    data_df["Status2"] = list(map(Status_Calc, data_df["stock_p_change"], data_df["sp500_p_change"]))

    X = np.array(data_df[FEATURES].values)
    X = preprocessing.scale(X)

    y = (data_df["Status2"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())

    Z = np.array(data_df[["stock_p_change", "sp500_p_change"]])

    return X, y, Z


def Analysis():
    test_size = 1
    X, y, Z = Build_Data_Set()

    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(X[:-test_size], y[:-test_size])

    data_df = pd.DataFrame.from_csv("forward_sample_NO_NA.csv")

    data_df = data_df.replace("N/A", 0).replace("NaN", 0)

    X = np.array(data_df[FEATURES].values)

    X = preprocessing.scale(X)

    Z = data_df["Ticker"].values.tolist()

    invest_list = []

    for i in range(len(X)):
        p = clf.predict(X[i])[0]
        if p == 1:
            invest_list.append(Z[i])

    return invest_list


final_list = []

loops = 8

for x in range(loops):
    stock_list = Analysis()
    for e in stock_list:
        final_list.append(e)

x = Counter(final_list)

print(30 * "_")
for each in x:
    if x[each] > loops - (loops / 3):
        print(each)
