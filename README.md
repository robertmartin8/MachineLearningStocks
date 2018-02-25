# MachineLearningStocks

This project uses python and scikit-learn to make stock predictions. The code is based on Sentdex's excellent
[machine learning tutorial](https://www.youtube.com/playlist?list=PLQVvvaa0QuDd0flgGphKCej-9jp-QdzZ3).

This was my first proper python project, as well as the first time I've used GitHub, so apologies for poor documentation and bad coding.

**Update as of February 2017:** Because a fair amount of people have expressed interest in this project, over the
next few weeks I am going to fix all the oustanding issues and modernise the project. 

**Update as of October 2017:** Basically, my coding ability has come a long way since I first wrote this project, as has my understanding of machine learning. 
I have continuously been developing a second iteration of this project, which is FAR more robust and sophisticated (though the general idea remains the same).
 I have better data, better machine learning algorithms, and correspondingly better performance. 
 At some stage, I may update this project on github, but I hope you understand my reluctance to give away alpha. 
 That being said, I suggest you use this project as a starting point: from experience,
  I can tell you that on this backbone you can probably build a profitable trading strategy. 

## Overview

The program looks at historical stock fundamentals (e.g PE ratio, Debt/equity etc), and also historical prices. The program then tries to 'learn' if there is any relationship between those fundamentals and the resulting change in price.

Then, we feed in the current stock fundamentals. The program should then output a list of stocks which have 'good fundamentals', which in the past have corresponded to a price increase.

Note that this repository *does not include* all the backtesting etc. It is just the final product. During the backtesting, I was getting returns of about 17%, which is quite a decent outperformance of the market.

All stocks are US based, from the S&P500. This also behaves as our benchmark.

## Data sources

We need three datasets:

1. Historical stock fundamentals
2. Historical stock price changes (including data for the S&P500).
3. Current stock prices.

### Historical stock fundamentals

This is actually very difficult to find. However, it turns out that there is a way to parse it from yahoo finance. I will not go into details, because [Sentdex has done it for us](https://pythonprogramming.net/data-acquisition-machine-learning/). On this page you will be able to find a file called `intraQuarter.zip`.

intraQuarter contains a subfolder called KeyStats, which contains fundamentals for all stocks in the S&P500 back to around 2003, sorted by stock.

### Historical stock price changes

For the historical stock prices, I used [Quandl](https://www.quandl.com/), which has a free python API.

Quandl has nicely cleaned data, but more importantly its stock data has been adjusted to include things like share splits.

The historical S&P500 values can be downloaded from [yahoo finance](https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC), which we name `YAHOO-INDEX_GSPC.csv`.

###  Current data

Current data is parsed from Yahoo finance using regex. I tend to have to fix this whenever yahoo changes their UI :(


## What each file does

### quandlData.py

Uses the quandl API to get historic adjusted stock prices, returning `stock_prices.csv`.

**update as of september 2017:** I suspect this is broken, because quandl changed their UI.
However, one can simply use this module 
 

### dataAcquisition.py

This is the bulk of the project. It looks through intraQuarter to parse the historical fundamental data into a pandas dataframe. Then, it adds to this dataframe the stock percentage change in a year. We compare this with the change in the S&P500 in the same year, to determine if the stock underperformed or outperformed.

Requires intraQuarter, `stock_prices.csv`, and `YAHOO-INDEX_GSPC.csv`.

Outputs a csv called `key_stats_NO_NA_enhanced.csv`.


### currentData.py

Parses the current stock fundamentals from sg.finance.yahoo, and puts them into a dataframe, finally returning a csv called `forward_sample_NO_NA.csv`.

### stockPrediction.py

The machine learning. Uses a linear SVM to fit the data, then predicts the outcome. Returns a list of stocks to invest in.

## Dependencies

Being lazy, I have copied all the unique import statements.

```python
import numpy as np
from sklearn import svm, preprocessing
import pandas as pd
from collections import Counter
import os
import re
import time
import urllib.request
from datetime import datetime
from Quandl import Quandl
```
