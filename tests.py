import pytest
import os
import pandas as pd

import current_data
import utils


def test_statspath():
    # Check that the statspath exists and is a directory
    assert os.path.exists(current_data.statspath)
    assert os.path.isdir(current_data.statspath)


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


def test_data_string_to_float():
    """
    This is a function that needs to meet lots of empirical requirements depending on the
    imperfections of Yahoo Finance's HTML. The main things are parsing negatives and
    abbreviations of big numbers.
    """

    assert utils.data_string_to_float("asdfNaN") == "N/A"
    assert utils.data_string_to_float(">N/A\n</") == "N/A"
    assert utils.data_string_to_float(">0") == 0
    assert utils.data_string_to_float("-3") == -3
    assert utils.data_string_to_float("4K") == 4000
    assert utils.data_string_to_float("2M") == 3000000
    assert utils.data_string_to_float("0.07B") == 70000000
    assert utils.data_string_to_float("-100.1K") == -100100
    assert utils.data_string_to_float("-0.1M") == -100000
    assert utils.data_string_to_float("-0.02B") == -20000000
    assert utils.data_string_to_float("-0.00") == 0
    assert utils.data_string_to_float("0.00") == 0
    assert utils.data_string_to_float("0M") == 0
    assert utils.data_string_to_float("010K") == 10000

    with pytest.raises(ValueError):
        utils.data_string_to_float(">0x")
    with pytest.raises(ValueError):
        utils.data_string_to_float("10k")
    with pytest.raises(ValueError):
        utils.data_string_to_float("2KB")
