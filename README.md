# MachineLearningStocks in python

MachineLearningStokcs is designed to be an intuitive and highly extensible 'template' project applying machine learning to making stock predictions.

Concretely, we clean and prepare a dataset of historical stock prices and fundamentals using `pandas`, then apply a `scikit-learn` classifier to discover the relationship between stock fundamentals (e.g PE ratio, debt/equity, float, etc) and the subsequent annual price change (compared with the index growth). We then conduct a simple backtest, before generating predictions on current data.

While I would not live trade based off of the predictions from this exact code, I do believe that you can use this project as starting point for a profitable trading system – I have actually used code based on this project to live trade, with pretty decent results (around 20% returns on backtest and 10-15% on live trading).

Though this project was originally based on Sentdex's excellent [machine learning tutorial](https://www.youtube.com/playlist?list=PLQVvvaa0QuDd0flgGphKCej-9jp-QdzZ3), it has quite a lot of personal significance for me. It was my first proper python project, one of my first real encounters with ML, and the first time I used git. At the start, my code was rife with bad practice and inefficiency: I have since tried to amend most of this, but please be warned that some minor issues may remain (feel free to raise an issue, or fork and submit a PR). Both the project and myself as a programmer have evolved a lot since the first iteration, and despite its origins in a youtube tutorial series I now think of it as 'my own'.

*As a disclaimer, this is a purely educational project. Be aware that backtested performance may often be deceptive – trade at your own risk!*

## Contents

- [Overview](#overview)
- [Quickstart](#quickstart)
- [Historical data](#historical-data)
  - [Historical stock fundamentals](#historical-stock-fundamentals)
  - [Historical stock price data](#historical-stock-price-data)
  - [Historical S&P500 prices](#historical-sp500-prices)
- [Preprocessing](#preprocessing)
  - [Features](#features)
    - [Valuation measures](#valuation-measures)
    - [Financials](#financials)
    - [Trading information](#trading-information)
- [Backtesting](#backtesting)
- [Current fundamental data](#current-fundamental-data)
  - [download_historical_prices.py](#downloadhistoricalpricespy)
  - [parse_keystats.py](#parsekeystatspy)
  - [currentData.py](#currentdatapy)
  - [stockPrediction.py](#stockpredictionpy)
- [Dependencies](#dependencies)
- [Unit testing](#unit-testing)
- [Where to go from here](#where-to-go-from-here)
  - [Data acquisition](#data-acquisition)
  - [Data preprocessing](#data-preprocessing)
  - [Machine learning](#machine-learning)

## Overview

The overall workflow to use machine learning to make stocks prediction is as follows:

1. Acquire historical fundamental data -- these are the *features* or *predictors*
2. Acquire historical stock price data -- this is will make up the dependent variable (what we are trying to predict).
3. Acquire historical index data (in this case, S&P500) -- a 5% stock growth does not mean much if the S&P500 grew 10% in that time period, so we will be comparing all returns to those of the index.
4. Preprocess data
5. Use a machine learning model to learn from your data
6. Backtest the performance of the machine learning model
7. Acquire current fundamental data
8. Generate predictions from current fundamental data

This is a very generalised overview, but in principle this is all you need to build a fundamentals-based ML stock predictor.

## Quickstart

If you want to throw away the instructions and play immediately, clone this project, then download and unzip the [data file](https://pythonprogramming.net/data-acquisition-machine-learning/) into the same directory.

Then, run the following in terminal:

```bash
python download_historical_prices.py
python parsing_keystats.py
python backtesting.py
python tests.py
python current_data.py
python stock_prediction.py
```

## Historical data

It turns out that data acquisition and processing is probably the hardest part of this project. But it is a prerequisite for any machine learning, so it's best to not fret and just carry on.

At this stage, we need three datasets:

1. Historical stock fundamentals
2. Historical stock prices
3. Historical S&P500 prices

### Historical stock fundamentals

Historical fundamental data is actually very difficult to find (for free, at least). Although sites like [Quandl](https://www.quandl.com/) do have datasets available, you often have to pay a pretty steep fee.

It turns out that there is a way to parse this data, for free, from [Yahoo finance](https://finance.yahoo.com/). I will not go into details, because [Sentdex has done it for us](https://pythonprogramming.net/data-acquisition-machine-learning/). On his page you will be able to find a file called `intraQuarter.zip`. Relevant to this project is the subfolder called `_KeyStats`, which contains html files that hold stock fundamentals for all stocks in the S&P500 back to around 2003, sorted by stock. However, at this stage, the data is unusable -- we have to parse it into a nice csv file.

### Historical stock price data

In the first iteration of the project, I used `pandas-datareader`, an extremely convenient library which can load stock data straight into pandas. However, after Yahoo Finance changed their UI, `datareader` no longer worked, so I switched to [Quandl](https://www.quandl.com/), which has a free python API (and free stock price data for a number of stocks).

However, as `pandas-datareader` has been [fixed](https://github.com/ranaroussi/fix-yahoo-finance), we will use it.

### Historical S&P500 prices

Likewise, we can easily use `pandas-datareader` to access data for the SPY ticker.

Failing that, one could manually download it from [yahoo finance](https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC) and place it into the project directory.

## Preprocessing

### Features

#### Valuation measures

- 'Market Cap'
- Enterprise Value
- Trailing P/E
- Forward P/E
- PEG Ratio
- Price/Sales
- Price/Book
- Enterprise Value/Revenue
- Enterprise Value/EBITDA

#### Financials

- Profit Margin
- Operating Margin
- Return on Assets
- Return on Equity
- Revenue
- Revenue Per Share
- Quarterly Revenue Growth
- Gross Profit
- EBITDA
- Net Income Avi to Common
- Diluted EPS
- Quarterly Earnings Growth
- Total Cash
- Total Cash Per Share
- Total Debt
- Total Debt/Equity
- Current Ratio
- Book Value Per Share
- Operating Cash Flow
- Levered Free Cash Flow

#### Trading information

- Beta
- 50-Day Moving Average
- 200-Day Moving Average
- Avg Vol (3 month)
- Shares Outstanding
- Float
- % Held by Insiders
- % Held by Institutions
- Shares Short
- Short Ratio
- Short % of Float
- Shares Short (prior month)

## Backtesting

Backetesting is arguably the most important part of any quantitative strategy: you must have some way of testing the performance of your algorithm before you live trade it.

Despite its importance, I originally did not want to include backtesting code in this repository. The reasons were as follows:

- Backtesting is messy and empirical. The code is not very pleasant to use, and requires a lot of manual interaction.
- Backtesting is very difficult to get right, and if you do it wrong, you will be deceiving yourself with high returns.
- Developing and working with your backtest is probably the best way to learn about machine learning and stocks -- you'll see what works, what doesn't, and what you don't understand.

Nevertheless, because of the importance of backtesting, I decided that I can't really call this a 'skeletal machine learning stocks' project without backtesting -- the skeleton would be missing the spine.

Thus, I have included a simplistic backtesting script. Please note that there is a fatal flaw with this backtesting implementation that will result in *much* higher backtesting returns. It is quite a subtle point, but I will let you figure that out :)

## Current fundamental data

Current data is scraped from Yahoo finance: we literally just download the statistics page for each stock (here is the [page](https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL) for Apple).

Then, we parse it using regex. In general, it is [really not recommended](https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags) to use regex to parse HTML. However, I think regex probably wins out for ease of understanding (this project being educational in nature), and from my experience regex works fine for this specific example.

This part of the projet has to be fixed whenever yahoo finance changes their UI.

### download_historical_prices.py

Uses `pandas-datareader` with the Yahoo Finance fix to download historical stock price and S&P500 price data.

### parse_keystats.py

This is the bulk of the project. It looks through intraQuarter to parse the historical fundamental data into a pandas dataframe. Then, it adds to this dataframe the stock percentage change in a year. We compare this with the change in the S&P500 in the same year, to determine if the stock underperformed or outperformed.

Requires intraQuarter, `stock_prices.csv`, and `YAHOO-INDEX_GSPC.csv`.

Outputs a csv called `key_stats_NO_NA_enhanced.csv`.

### currentData.py

Parses the current stock fundamentals from sg.finance.yahoo, and puts them into a dataframe, finally returning a csv called `forward_sample_NO_NA.csv`.

### stockPrediction.py

The machine learning. Uses a linear SVM to fit the data, then predicts the outcome. Returns a list of stocks to invest in.

## Dependencies

- pandas

## Unit testing

I have included a number of unit tests (in the `tests/` folder) which serve to check that things are working properly. However, due to the nature of the some of this projects functionality (downloading big datasets), you will have to run all the code once before running the tests. Otherwise, the tests themselves would have to download huge datasets (which I don't think is optimal).

To run the tests, simply enter the following into a terminal instance in the project directory:

```bash
pytest -v
```

## Where to go from here

I have stated that this project is extensible, so here are some ideas to get you started (and increase returns)

### Data acquisition

My personal belief is that better quality data is THE factor that will determine your ultimate performance. Here are some ideas:

- Explore the other subfolders in Sentdex's `intraQuarter.zip`.
- Parse the annual reports that all companies submit to the SEC (have a look at the [Edgar Database](https://www.sec.gov/edgar/searchedgar/companysearch.html))
- Try to find websites from which to scrape fundamental data (this has been my solution).
- Ditch US stocks and go global -- perhaps better results may be found in markets that are less-liquid. It'd be interesting to see whether the predictive power of features vary based on geography.
- Buy Quandl data, or experiment with alternative data.

### Data preprocessing

- Build a more robust parser using BeautifulSoup
- In this project, I have just ignored any rows with missing data, but this reduces the size of the dataset considerably. Are there any ways you can fill in some of this data?
  - hint: if the PE ratio is missing but you know the stock price and the earnings/share...
  - hint 2: how different is Apple's book value in March to its book value in June?
- Some form of feature engineering: e.g, calculate [Graham's number](https://www.investopedia.com/terms/g/graham-number.asp) and use it as a feature!
- Experiment with different values of the `outperformance` parameter

### Machine learning

Altering the machine learning stuff is probably the easiest and most fun.

- Try some parameter tuning
- Try a different classifier -- there is plenty of research that advocates the use of SVMs, for example. Don't forget that other classifiers may require feature scaling etc.
- Make it *deep* -- experiment with neural networks (an easy way to start is with `sklearn.neural_network`).
- Change the classification problem into a regresion one: will we achieve better results if we try to predict the stock *price* rather than whether it outperformed?
- Run the prediction multiple times (perhaps using different hyperparameters?) and select the *k* most common stocks to invest in. This is especially important if the algorithm is not deterministic (as is the case for Random Forest)
