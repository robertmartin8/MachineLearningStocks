import pytest
import os
import pandas as pd

import parsing_keystats
import stock_prediction
import download_historical_prices
import current_data
import utils


def test_forward_sample_dimensions():
    """
    Check that the forward sample has been built correctly
    """
    # Number of features + ['Date', 'Unix', 'Ticker', 'Price', 'stock_p_change', 'SP500', 'SP500_p_change']
    df = pd.read_csv('forward_sample.csv')
    indexing_columns = ['Date', 'Unix', 'Ticker', 'Price',
                        'stock_p_change', 'SP500', 'SP500_p_change']
    n_cols = len(df.columns)
    assert n_cols == len(current_data.features) + len(indexing_columns)
    assert len(df) == len(os.listdir('forward/'))
    indexing_columns.remove('Ticker')
    # Make sure that all of the indexing columns only contain zeroes
    assert df[indexing_columns].sum().sum() == 0


def test_forward_sample_data():
    """
    Some quick checks on the data
    """
    df = pd.read_csv('forward_sample.csv')
    # For these tests we need to fill in nan values with zero
    df.fillna(0, inplace=True)

    # Make sure that these features have positive values
    positive_features = ['Market Cap', 'Price/Sales', 'Revenue', 'Revenue Per Share', 'Total Cash',
                         'Total Cash Per Share', 'Total Debt', '50-Day Moving Average', '200-Day Moving Average',
                         'Avg Vol (3 month)', 'Shares Outstanding', 'Float',
                         '% Held by Insiders', '% Held by Institutions', 'Shares Short',
                         'Short Ratio', 'Short % of Float', 'Shares Short (prior month)']
    assert all(df[positive_features] >= 0)

    # Make sure that these features have values less than 100 (the above checks that they are +ve)
    fractional_features = ['% Held by Insiders', '% Held by Institutions',
                           'Short Ratio', 'Short % of Float']
    assert all(df[fractional_features] <= 100)


@pytest.mark.xfail()
def test_stock_prediction_dataset():
    """
    This tests that the dataset on which we are training our algorithm has been correctly built
    """
    df = pd.read_csv("keystats.csv", index_col='Date')
    X, y = stock_prediction.build_data_set()
    assert X.shape[0] == df.shape[0]
    assert len(y) == df.shape[0]
    assert X.shape[1] == len(parsing_keystats.features)
