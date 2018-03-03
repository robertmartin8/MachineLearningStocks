def data_string_to_float(number_string):
    """
    The result of our regex search is a number stored as a string, but we need a float.
    Some of these strings say things like '25M' instead of 25000000. Some are negative,
    i.e the digits are preceded by '-'. Some have 'N/A' in them.
    As an artifact of our regex, some values which were meant to be zero are instead '>0'.
We must process all of these cases accordingly.
    :param number_string: the string output of our regex, which needs to be converted to a float.
    :return: a float representation of the string, taking into account minus sign, unit, etc.
    """
    if ("N/A" in number_string) or ("NaN" in number_string):
        return "N/A"
    elif number_string == ">0":
        return 0
    elif "-" in number_string:
        number_string = number_string.replace("-", '')
        if "B" in number_string:
            return float(number_string.replace("B", '')) * -1000000000
        elif "M" in number_string:
            return float(number_string.replace("M", '')) * -1000000
        elif "K" in number_string:
            return float(number_string.replace("K", '')) * -1000
        else:
            return -float(number_string)

    elif "B" in number_string:
        return float(number_string.replace("B", '')) * 1000000000
    elif "M" in number_string:
        return float(number_string.replace("M", '')) * 1000000
    elif "K" in number_string:
        return float(number_string.replace("K", '')) * 1000
    else:
        return float(number_string)
