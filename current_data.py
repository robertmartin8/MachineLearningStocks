import pandas as pd
import os
import re
import time
import urllib.request

# Enter the file path to the intraQuarter directory
path = "/Users/User/intraQuarter"


def check_yahoo():
    """
    Retrieves the stock ticker from intraQuarter, then downloads the html file from yahoo finance.
    :return: forward/ filled with the html file for each ticker
    """
    statspath = path + '/_KeyStats/'
    stock_list = [x[0] for x in os.walk(statspath)]

    # Parse yahoo finance based on these tickers
    for each_dir in stock_list[1:]:
        try:
            # Get the ticker from intraQuarter
            ticker = each_dir.split(statspath)[1]
            link = "http://finance.yahoo.com/quote/" + ticker.upper() + "/key-statistics"
            resp = urllib.request.urlopen(link).read()

            # Write results to forward/
            save = "forward/" + str(ticker) + ".html"
            file = open(save, "w")
            file.write(str(resp))
            file.close()

            print(save)

        except Exception as e:
            print(str(e))
            time.sleep(2)


def forward():
    """
    Creates the forward sample, by parsing the html that we downloaded in check_yahoo(). 
    Reads this data into a dataframe, then converts to a csv. 
    :return: the forward sample as a csv. 
    """
    # The parameters which we will search for
    gather = ["Total Debt/Equity",
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
              'Net Income Avi to Common',
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
              'Shares Short',
              'Short Ratio',
              'Short % of Float',
              'Shares Short (prior ']

    # The empty dataframe which we will fill
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

    file_list = os.listdir("forward")

    # This is a requirement if you are on a mac. Inelegant code just to remove the DS_store.
    # Thanks Apple!
    if '.DS_Store' in file_list:
        del file_list[file_list.index('.DS_Store')]

    # This is the actual parsing. This needs to be fixed every time yahoo changes their UI.
    for each_file in file_list:
        ticker = each_file.split(".html")[0]
        full_file_path = "forward/" + each_file
        source = open(full_file_path, "r").read()

        try:
            value_list = []

            for each_data in gather:
                try:
                    regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                    value = re.search(regex, source)
                    value = (value.group(1))

                    if "B" in value:
                        value = float(value.replace("B", '')) * 1000000000
                    elif "M" in value:
                        value = float(value.replace("M", '')) * 1000000

                    value_list.append(value)

                except Exception:
                    value = 'N/A'
                    value_list.append(value)

            if value_list.count("N/A") > 0:
                # This is why our result is 'forward_sample_NO_NA'. Change this if you want NA.
                # But of course, in that case you need to deal with the NA later on.
                pass

            else:
                print(each_file)

                # I know this is ugly, but it's practical.
                df = df.append({'Date': "N/A",
                                'Unix': "N/A",
                                'Ticker': ticker,
                                'Price': "N/A",
                                'stock_p_change': "N/A",
                                'SP500': "N/A",
                                'sp500_p_change': "N/A",
                                'Difference': "N/A",
                                'DE Ratio': value_list[0],
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
                                'Status': "N/A"}, ignore_index=True)

        except Exception:
            pass

        df.to_csv("forward_sample_NO_NA.csv")


# Call the functions to produce the csv.
check_yahoo()
forward()
