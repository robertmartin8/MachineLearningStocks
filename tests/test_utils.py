import pytest
import utils


def test_status_calc():
    """
    Test the status_calc function which generates training labels
    """
    assert utils.status_calc(50, 20, 12.2) == 1
    assert utils.status_calc(12.003, 10, 15) == 0
    assert utils.status_calc(-10, -30, 5) == 1
    assert utils.status_calc(-31, -30, 15) == 0
    assert utils.status_calc(15, 5, 10) == 1

    with pytest.raises(ValueError):
        utils.status_calc(12, 10, -3)


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
        utils.data_string_to_float("2KB")


def test_data_string_to_float_case_insensitive():
    """
    Bug Fix 3: data_string_to_float should be case-insensitive for K, M, B suffixes.
    This test verifies that both uppercase and lowercase unit suffixes are handled correctly.
    """
    # Test lowercase 'k', 'm', 'b'
    assert utils.data_string_to_float("10k") == 10000
    assert utils.data_string_to_float("5m") == 5000000
    assert utils.data_string_to_float("2.5b") == 2500000000

    # Test mixed case
    assert utils.data_string_to_float("10K") == 10000
    assert utils.data_string_to_float("10k") == 10000
    assert utils.data_string_to_float("5M") == 5000000
    assert utils.data_string_to_float("5m") == 5000000

    # Test negative values with lowercase
    assert utils.data_string_to_float("-100.1k") == -100100
    assert utils.data_string_to_float("-0.1m") == -100000
    assert utils.data_string_to_float("-0.02b") == -20000000

    # Test NaN variations
    assert utils.data_string_to_float("nan") == "N/A"
    assert utils.data_string_to_float("NaN") == "N/A"
    assert utils.data_string_to_float("NAN") == "N/A"
    assert utils.data_string_to_float("n/a") == "N/A"
    assert utils.data_string_to_float("N/a") == "N/A"
