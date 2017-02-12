# MachineLearningStocks

This project uses python and scikit-learn to make stock predictions. The code is based on Sentdex's excellent
[machine learning tutorial](https://www.youtube.com/playlist?list=PLQVvvaa0QuDd0flgGphKCej-9jp-QdzZ3).

This was my first proper python project, as well as the first time I've used GitHub, so apologies for poor documentation and bad coding.

## Overview

The program looks at historical stock fundamentals (e.g PE ratio, Debt/equity etc), and also historical prices. The program then tries to 'learn' if there is any relationship between those fundamentals and the resulting change in price.

Then, we feed in the current stock fundamentals. The program should then output a list of stocks which have 'good fundamentals', which in the past have corresponded to a price increase.

Note that this project *does not include* all the backtesting etc. It is just the final product. During the backtesting, I was getting returns of about 17%, which is quite a decent outperformance of the market.

All stocks are US based, from the S&P500. This also behaves as our benchmark.

## Data sources

We need three datasets:

1. Historical stock fundamentals
2. Historical stock price changes (including data for the S&P500).
3. Current stock prices.

### Historical stock fundamentals

This is actually very difficult to find. However, it turns out that there is a way to parse it from yahoo finance. I do not know how to do this. Fortunately, [Sentdex has done it for us](https://pythonprogramming.net/data-acquisition-machine-learning/). On this page you will be able to find a file called intraQuarter.zip,

intraQuarter contains a subfolder called KeyStats, which contains fundamentals for all stocks in the S&P500 back to around 2003, sorted by stock.

### Historical stock price changes

For the historical stock prices, I used [Quandl](https://www.quandl.com/), which has a free python API.

Quandl has nicely cleaned data, but more importantly its stock data has been adjusted to include things like share splits.


###  Current data

Current data is parsed from Yahoo finance. The original code did the parsing using regex, but since the code was written Yahoo massively changed their UI. As such, we actually parse the data from Yahoo Finance Singapore, which still uses the old UI. Once this UI is changed, the program will no longer work.


### What each file does


## Usage



## Dependencies
