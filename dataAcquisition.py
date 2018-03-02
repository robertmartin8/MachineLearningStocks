import pandas as pd
import os
import time
import re
from datetime import datetime

# How much a stock has to outperform the S&P500 to be considered a success. Subjective.
how_much_better = 5

# Enter the path to intraQuarter
path = "/Users/User/intraQuarter"


# The list of features we will be looking at. No choice but to hard code it.
def key_stats(gather=["Total Debt/Equity",
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
                      'Shares Short (prior ']):
    """
    Looks at the data parsed for us by Sentdex (in intraQuarter) to make a csv of the historical
    key statistics.
    :param gather: The list of fundamentals which we need to gather.
    :return: csv of historical key statistics, on which we will train our SVM.
    """

    # List of stocks
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'Price',
                               'stock_p_change',
                               'SP500',
                               'sp500_p_change',
                               'Difference',
                               'DE Ratio',
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
                               'Shares Short (prior ',
                               'Status'])

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    stock_df = pd.DataFrame.from_csv("stock_prices.csv")

    ticker_list = []

    # For each stock, we create a list containing all of the different data files
    # (corresponding to different dates.)
    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)

        # snippet to get rid of the stupid .DS_Store file that osx makes.
        if '.DS_Store' in each_file:
            del each_file[each_file.index('.DS_Store')]

        ticker = each_dir.split(statspath)[1]  # retrieves the stock symbol
        ticker_list.append(ticker)

        if len(each_file) > 0:  # checking that the data exists
            for file in each_file:

                # Retrieve the datestamp, and convert to unix format.
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())

                full_file_path = each_dir + '/' + file
                source = open(full_file_path, 'r').read()

                try:
                    value_list = []

                    for each_data in gather:
                        try:
                            # Use a regex to find the value associated with the variable of interest.
                            regex = re.escape(
                                each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                            value = re.search(regex, source)
                            value = (value.group(1))

                            if "B" in value:
                                value = float(value.replace(
                                    "B", '')) * 1000000000
                            elif "M" in value:
                                value = float(value.replace("M", '')) * 1000000

                            value_list.append(value)

                        except Exception:
                            value = 'N/A'
                            value_list.append(value)

                    try:
                        sp500_date = datetime.fromtimestamp(
                            unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                    except:
                        # this except statement is in case we end up looking for data on a weekend,
                        # if this is the case, we subtract three days
                        try:
                            sp500_date = datetime.fromtimestamp(
                                unix_time - 259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_date)]
                            sp500_value = float(row["Adj Close"])
                        except Exception as e:
                            print("sp500", str(e))

                    # We want to see the stock's performance one year later.
                    one_year_later = int(unix_time + 31536000)

                    try:
                        sp500_1y = datetime.fromtimestamp(
                            one_year_later).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_1y)]
                        sp500_1y_value = float(row["Adj Close"])
                    except:
                        try:
                            # Again, for the case that we query data on a weekend
                            sp500_1y = datetime.fromtimestamp(
                                one_year_later - 259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_1y)]
                            sp500_1y_value = float(row["Adj Close"])
                        except Exception as e:
                            print("sp500 1 year later issue", str(e))

                    try:
                        stock_price_1y = datetime.fromtimestamp(
                            one_year_later).strftime('%Y-%m-%d')
                        row = stock_df[(stock_df.index ==
                                        stock_price_1y)][ticker.upper()]

                        stock_1y_value = round(float(row), 2)

                    except Exception as e:
                        try:
                            stock_price_1y = datetime.fromtimestamp(
                                one_year_later - 259200).strftime('%Y-%m-%d')
                            row = stock_df[(stock_df.index ==
                                            stock_price_1y)][ticker.upper()]
                            stock_1y_value = round(float(row), 2)
                        except Exception as e:
                            print("stock price:", str(e))

                    try:
                        stock_price = datetime.fromtimestamp(
                            unix_time).strftime('%Y-%m-%d')
                        row = stock_df[(stock_df.index ==
                                        stock_price)][ticker.upper()]
                        stock_price = round(float(row), 2)

                    except Exception as e:
                        try:
                            stock_price = datetime.fromtimestamp(
                                unix_time - 259200).strftime('%Y-%m-%d')
                            row = stock_df[(stock_df.index ==
                                            stock_price)][ticker.upper()]
                            stock_price = round(float(row), 2)
                        except Exception as e:
                            print("stock price:", str(e))

                    stock_p_change = round(
                        ((stock_1y_value - stock_price) / stock_price * 100), 2)
                    sp500_p_change = round(
                        ((sp500_1y_value - sp500_value) / sp500_value * 100), 2)

                    # If the stock outperformed the SP500 by 5%, label it 'outperform'.
                    if stock_p_change - sp500_p_change > how_much_better:
                        status = "outperform"
                    else:
                        status = "underperform"

                    # This determines if we have NA or no NA
                    if value_list.count("N/A") > 0:
                        pass
                    else:
                        df = df.append({'Date': date_stamp,
                                        'Unix': unix_time,
                                        'Ticker': ticker,
                                        'Price': stock_price,
                                        'stock_p_change': stock_p_change,
                                        'SP500': sp500_value,
                                        'sp500_p_change': sp500_p_change,
                                        'Difference': stock_p_change - sp500_p_change,
                                        'DE Ratio': value_list[0],
                                        # 'Market Cap': value_list[1],
                                        'Trailing P/E': value_list[1],
                                        'Price/Sales': value_list[2],
                                        'Price/Book': value_list[3],
                                        'Profit Margin': value_list[4],
                                        'Operating Margin': value_list[5],
                                        'Return on Assets': value_list[6],
                                        'Return on Equity': value_list[7],
                                        'Revenue Per Share': value_list[8],
                                        'Market Cap': value_list[9],
                                        'Enterprise Value': value_list[10],
                                        'Forward P/E': value_list[11],
                                        'PEG Ratio': value_list[12],
                                        'Enterprise Value/Revenue': value_list[13],
                                        'Enterprise Value/EBITDA': value_list[14],
                                        'Revenue': value_list[15],
                                        'Gross Profit': value_list[16],
                                        'EBITDA': value_list[17],
                                        'Net Income Avl to Common ': value_list[18],
                                        'Diluted EPS': value_list[19],
                                        'Earnings Growth': value_list[20],
                                        'Revenue Growth': value_list[21],
                                        'Total Cash': value_list[22],
                                        'Total Cash Per Share': value_list[23],
                                        'Total Debt': value_list[24],
                                        'Current Ratio': value_list[25],
                                        'Book Value Per Share': value_list[26],
                                        'Cash Flow': value_list[27],
                                        'Beta': value_list[28],
                                        'Held by Insiders': value_list[29],
                                        'Held by Institutions': value_list[30],
                                        'Shares Short (as of': value_list[31],
                                        'Short Ratio': value_list[32],
                                        'Short % of Float': value_list[33],
                                        'Shares Short (prior ': value_list[34],
                                        'Status': status}, ignore_index=True)
                except Exception as e:
                    # This is awful practice from an awful coder.
                    pass

    df.to_csv("key_stats_NO_NA_enhanced.csv")


# Call the function to produce the csv
key_stats()
