import urllib.request
import os
import time

# Creates a directory with the current stock fundamentals.

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
