import pytest

import utils
import stock_prediction


def test_status_calc():
    """
    Test the status_calc function which generates training labels
    """
    assert stock_prediction.status_calc(50, 20, 12.2) == 1
    assert stock_prediction.status_calc(12.003, 10, 15) == 0
    assert stock_prediction.status_calc(-10, -30, 5) == 1
    assert stock_prediction.status_calc(-31, -30, 15) == 0
    assert stock_prediction.status_calc(15, 5, 10) == 1

    with pytest.raises(ValueError):
        stock_prediction.status_calc(12, 10, -3)


def test_data_string_to_float():
    """
    data_string_to_float() is a function that needs to meet lots of empirical requirements
    owing to the idiosyncrasies of Yahoo Finance's HTML. The main jobs are parsing negatives and
    abbreviations of big numbers.
    """
    assert utils.data_string_to_float("asdfNaN") == "N/A"
    assert utils.data_string_to_float(">N/A\n</") == "N/A"
    assert utils.data_string_to_float(">0") == 0
    assert utils.data_string_to_float("-3") == -3
    assert utils.data_string_to_float("4K") == 4000
    assert utils.data_string_to_float("2M") == 2000000
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
