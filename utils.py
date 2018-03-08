def data_string_to_float(number_string):
    """
    The result of our regex search is a number stored as a string, but we need a float.
        - Some of these strings say things like '25M' instead of 25000000.
        - Some have 'N/A' in them.
        - Some are negative (have '-' in front of the numbers).
        - As an artifact of our regex, some values which were meant to be zero are instead '>0'.
    We must process all of these cases accordingly.
    :param number_string: the string output of our regex, which needs to be converted to a float.
    :return: a float representation of the string, taking into account minus sign, unit, etc.
    """
    # Deal with zeroes and the sign
    if ("N/A" in number_string) or ("NaN" in number_string):
        return "N/A"
    elif number_string == ">0":
        return 0
    elif "B" in number_string:
        return float(number_string.replace("B", '')) * 1000000000
    elif "M" in number_string:
        return float(number_string.replace("M", '')) * 1000000
    elif "K" in number_string:
        return float(number_string.replace("K", '')) * 1000
    else:
        return float(number_string)


def duplicate_error_check(df):
    """
    A common symptom of failed parsing is when there are consecutive duplicate values. This function was used
    to find the duplicates and tweak the regex. Any remaining duplicates are probably coincidences.
    :param df: the dataframe to be checked
    :return: Prints out a list of the rows containing duplicates, as well as the duplicated values.
    """
    # Some columns often (correctly) have the same value as other columns. Remove these.
    df.drop(['Unix', 'Price', 'stock_p_change', 'SP500', 'SP500_p_change', 'Float', '200-Day Moving Average', 'Short Ratio',
             'Operating Margin'], axis=1, inplace=True)

    for i in range(len(df)):
        # Check if there are any duplicates.
        if pd.Series(df.iloc[i] == df.iloc[i].shift()).any():
            duplicates = set([x for x in list(df.iloc[i])
                              if list(df.iloc[i]).count(x) > 1])
            # A duplicate value of zero is quite common. We want other duplicates.
            if duplicates != {0}:
                print(i, df.iloc[i], duplicates, sep="\n")


def status_calc(stock, sp500, outperformance=10):
    """A simple function to classify whether a stock outperformed the S&P500
    :param stock: stock price
    :param sp500: S&P500 price
    :param outperformance: stock is classified 1 if stock price > S&P500 price + outperformance
    :return: true/false
    """
    if outperformance < 0:
        raise ValueError("outperformance must be positive")
    return stock - sp500 >= outperformance
