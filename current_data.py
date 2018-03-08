import pandas as pd
import os
import re
import time
import requests
import numpy as np
from utils import data_string_to_float

# The path to your fundamental data
statspath = "intraQuarter/_KeyStats/"

# These are the features that will be parsed
features = [  # Valuation measures
    'Market Cap',
    'Enterprise Value',
    'Trailing P/E',
    'Forward P/E',
    'PEG Ratio',
    'Price/Sales',
    'Price/Book',
    'Enterprise Value/Revenue',
    'Enterprise Value/EBITDA',
    # Financials
    'Profit Margin',
    'Operating Margin',
    'Return on Assets',
    'Return on Equity',
    'Revenue',
    'Revenue Per Share',
    'Quarterly Revenue Growth',
    'Gross Profit',
    'EBITDA',
    'Net Income Avi to Common',
    'Diluted EPS',
    'Quarterly Earnings Growth',
    'Total Cash',
    'Total Cash Per Share',
    'Total Debt',
    'Total Debt/Equity',
    'Current Ratio',
    'Book Value Per Share',
    'Operating Cash Flow',
    'Levered Free Cash Flow',
    # Trading information
    'Beta',
    '50-Day Moving Average',
    '200-Day Moving Average',
    'Avg Vol (3 month)',
    'Shares Outstanding',
    'Float',
    '% Held by Insiders',
    '% Held by Institutions',
    'Shares Short',
    'Short Ratio',
    'Short % of Float',
    'Shares Short (prior month)']


def check_yahoo():
    """
    Retrieves the stock ticker from the _KeyStats directory, then downloads the html file from yahoo finance.
    :return: a directory named `forward/` filled with the html files for each ticker
    """
    # Create the directory where we will store the current data
    if not os.path.exists('forward/'):
        os.makedirs('forward/')

    # Retrieve a list of tickers from the fundamental data folder
    ticker_list = os.listdir(statspath)

    # Required in macOS to remove the hidden index file.
    if '.DS_Store' in ticker_list:
        ticker_list.remove('.DS_Store')

    for ticker in ticker_list:
        try:
            link = f"http://finance.yahoo.com/quote/{ticker.upper()}/key-statistics"
            resp = requests.get(link)

            # Write results to forward/
            save = f"forward/{ticker}.html"
            with open(save, 'w') as file:
                file.write(resp.text)
            print(save)

        except Exception as e:
            print(f"{ticker}: {str(e)}\n")
            time.sleep(2)


def forward():
    """
    Creates the forward sample by parsing the current data html files that we downloaded in check_yahoo().
    :return: a pandas dataframe containing all of the current data for each ticker.
    """
    # Creating an empty dataframe which we will later fill. In addition to the features, we need some index variables
    # (date, unix timestamp, ticker), and of course the dependent variables (prices).
    df_columns = ['Date',
                  'Unix',
                  'Ticker',
                  'Price',
                  'stock_p_change',
                  'SP500',
                  'SP500_p_change'] + features

    df = pd.DataFrame(columns=df_columns)

    tickerfile_list = os.listdir('forward/')

    # Required in macOS to remove the hidden index file.
    if '.DS_Store' in tickerfile_list:
        ticker_list.remove('.DS_Store')

    # This is the actual parsing. This needs to be fixed every time yahoo changes their UI.
    for tickerfile in tickerfile_list:
        ticker = tickerfile.split('.html')[0].upper()
        source = open(f"forward/{tickerfile}").read()
        # Remove commas from the html to make parsing easier.
        source = source.replace(',', '')

        # Regex search for the different variables in the html file, then append to value_list
        value_list = []
        for variable in features:
            try:
                # Basically, look for the first number present after we an occurence of the variable
                regex = r'>' + re.escape(variable) + r'.*?(\-?\d+\.*\d*K?M?B?|N/A[\\n|\s]*|>0|NaN)%?' \
                                                     r'(</td>|</span>)'
                value = re.search(regex, source, flags=re.DOTALL).group(1)

                # Dealing with number formatting
                value_list.append(data_string_to_float(value))

            # The data may not be present. Process accordingly.
            except AttributeError:
                value_list.append('N/A')
                print(ticker, variable)

        # Append the ticker and the features to the dataframe
        new_df_row = [0, 0, ticker,
                      0, 0, 0, 0] + value_list

        df = df.append(dict(zip(df_columns, new_df_row)), ignore_index=True)

    return df.replace('N/A', np.nan)


if __name__ == '__main__':
    check_yahoo()
    current_df = forward()
    current_df.to_csv('forward_sample.csv', index=False)
