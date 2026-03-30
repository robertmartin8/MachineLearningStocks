import os
import pandas as pd
import pytest

import parsing_keystats
import stock_prediction
import current_data


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
    Some quick checks on the forward sample data
    """
    df = pd.read_csv('forward_sample.csv')
    # For these tests we need to fill in nan values with zero
    df.fillna(0, inplace=True)

    # Make sure that these features have positive values
    positive_features = ['Market Cap', 'Price/Sales', 'Revenue', 'Revenue Per Share', 'Total Cash',
                         'Total Cash Per Share', 'Total Debt', '50-Day Moving Average', '200-Day Moving Average',
                         'Avg Vol (3 month)', 'Shares Outstanding', 'Float',
                         '% Held by Insiders', '% Held by Institutions', 'Shares Short',
                         'Short Ratio', 'Short % of Float', 'Shares Short (prior month']
    assert all(df[positive_features] >= 0)

    # Make sure that these features have values less than 100 (the above checks that they are +ve)
    fractional_features = ['% Held by Insiders', '% Held by Institutions',
                           'Short Ratio', 'Short % of Float']
    assert all(df[fractional_features] <= 100)


def test_stock_prices_dataset():
    """
    Check that data from pandas-datareader has been downloaded correctly
    """

    df = pd.read_csv("stock_prices.csv", index_col='Date', parse_dates=True)
    assert type(df.index) == pd.core.indexes.datetimes.DatetimeIndex
    # Make sure that all columns have some price data
    assert all(df.isnull().sum() < len(df))
    # After this, we fill in missing values with zero for test purposes
    df.fillna(0, inplace=True)
    assert all(df >= 0)

    # Index prices
    index_df = pd.read_csv(
        "sp500_index.csv", index_col='Date', parse_dates=True)
    assert type(df.index) == pd.core.indexes.datetimes.DatetimeIndex
    assert len(index_df.columns) == 6
    assert index_df.shape[0] == df.shape[0]
    assert index_df.isnull().sum().sum() == 0


def def_keystats_dimensions():
    """
    This tests that the keystats csv has been built correctly
    """
    df = pd.read_csv("keystats.csv", index_col='Date')

    indexing_columns = ['Unix', 'Ticker', 'Price',
                        'stock_p_change', 'SP500', 'SP500_p_change']
    n_cols = len(df.columns)
    assert n_cols == len(parsing_keystats.features) + len(indexing_columns)

    # No missing data in the index columns
    assert df[indexing_columns].isnull().sum().sum() == 0


def test_stock_prediction_dataset():
    """
    This tests that the dataset on which we are training our algorithm has been correctly built
    """
    df = pd.read_csv("keystats.csv", index_col='Date')
    num_rows_with_nan = sum(df.isnull().sum(axis=1) > 0)

    X, y = stock_prediction.build_data_set()
    assert X.shape[0] == df.shape[0] - num_rows_with_nan
    assert len(y) == df.shape[0] - num_rows_with_nan
    assert X.shape[1] == len(parsing_keystats.features)


def test_features_names_complete():
    """
    Bug Fix 2: Feature names should be complete and consistent.
    This test verifies that feature names have proper parentheses matching.
    """
    for feature in parsing_keystats.features:
        # Check that parentheses are balanced
        open_count = feature.count('(')
        close_count = feature.count(')')
        assert open_count == close_count, f"Feature '{feature}' has unbalanced parentheses"


def test_pandas_append_deprecated_fix():
    """
    Bug Fix 1: pandas.DataFrame.append is deprecated.
    This test verifies that parse_keystats no longer uses the deprecated append method.
    Instead, it should collect rows in a list and create the DataFrame at the end.
    """
    import inspect
    source = inspect.getsource(parsing_keystats.parse_keystats)

    # Verify that append is not used on DataFrame
    assert ".append(" not in source, "parse_keystats should not use deprecated DataFrame.append()"

    # Verify that the new pattern is used (collecting rows in a list)
    assert "df_rows = []" in source, "parse_keystats should use list to collect rows"
    assert "df_rows.append(" in source, "parse_keystats should append to list, not DataFrame"
    assert "pd.DataFrame(df_rows" in source, "parse_keystats should create DataFrame from list"
