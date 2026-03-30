import os
import parsing_keystats
import current_data
import stock_prediction


def test_statspath():
    # Check that the statspath exists and is a directory
    assert os.path.exists(current_data.statspath)
    assert os.path.isdir(current_data.statspath)

    assert parsing_keystats.statspath == current_data.statspath


def test_features_same():
    assert set(parsing_keystats.features) == set(current_data.features)


def test_outperformance():
    assert stock_prediction.OUTPERFORMANCE >= 0
