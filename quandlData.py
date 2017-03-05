import pandas as pd
import os
from Quandl import Quandl

# Obviously replace with your own path and API key.
path = "/Users/User/intraQuarter"
auth_tok = "enteryourkey"


def stock_prices():
    df = pd.DataFrame()
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split("/Users/User/intraQuarter/_KeyStats/")[1]
            print(ticker)
            name = "WIKI/" + ticker.upper()

            # Query Quandl, using the standard format, e.g WIKI/AAPL.
            data = Quandl.get(name,
                              trim_start="2000-12-12",
                              trim_end="2014-12-30",
                              authtoken=auth_tok)
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis=1)

        except Exception as e:
            print(str(e))

    df.to_csv("stock_prices.csv")


stock_prices()
