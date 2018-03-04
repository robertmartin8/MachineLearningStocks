import pytest
import os
import parsing_keystats
import current_data
import download_historical_prices


def test_statspath():
    # Check that the statspath exists and is a directory
    assert os.path.exists(current_data.statspath)
    assert os.path.isdir(current_data.statspath)

    assert parsing_keystats.statspath == current_data.statspath


def test_features_same():
    # There are only four differences (intentionally)
    assert set(parsing_keystats.features) - set(current_data.features) == {'Qtrly Revenue Growth', 'Qtrly Earnings Growth',
                                                                           'Shares Short (as of', 'Net Income Avl to Common'}
    assert set(current_data.features) - set(parsing_keystats.features) == {'Net Income Avi to Common', 'Quarterly Earnings Growth',
                                                                           'Shares Short', 'Quarterly Revenue Growth'}


def test_dates_same():
    assert parsing_keystats.START_DATE == download_historical_prices.START_DATE
    assert parsing_keystats.END_DATE == download_historical_prices.END_DATE
