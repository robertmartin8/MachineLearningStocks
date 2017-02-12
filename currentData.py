import pandas as pd
import os
import re
import time
import urllib.request

path = "/Users/User/intraQuarter"


def check_yahoo():
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    for each_dir in stock_list[1:]:
        try:
            each_dir = each_dir.split("/Users/User/intraQuarter/_KeyStats/")[1]
            link = "http://sg.finance.yahoo.com/q/ks?s=" + each_dir.upper() + "+Key+Statistics"
            resp = urllib.request.urlopen(link).read()

            save = "forward/" + str(each_dir) + ".html"
            store = open(save, "w")
            store.write(str(resp))
            store.close()

        except Exception as e:
            print(str(e))
            time.sleep(2)


check_yahoo()


# This code puts the current data made by check_yahoo() into a dataframe then csv.


def forward(gather=["Total Debt/Equity",
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
    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'Price',
                               'stock_p_change',
                               'SP500',
                               'sp500_p_change',
                               'Difference',
                               ##############
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
                               ##############
                               'Status'])

    file_list = os.listdir("forward")

    if '.DS_Store' in file_list:
        idx = file_list.index('.DS_Store')
        del file_list[idx]

    print(file_list)

    for each_file in file_list[0:]:
        ticker = each_file.split(".html")[0]  # retrieves the stock symbol
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
                pass
            else:
                df = df.append({'Date': "N/A",
                                'Unix': "N/A",
                                'Ticker': ticker,
                                'Price': "N/A",
                                'stock_p_change': "N/A",
                                'SP500': "N/A",
                                'sp500_p_change': "N/A",
                                'Difference': "N/A",
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
                                'Status': "N/A"}, ignore_index=True)
        except Exception:
            pass

        df.to_csv("forward_sample_NO_NA.csv")


forward()
