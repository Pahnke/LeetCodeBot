import constants

''' CASTING FUNCS '''


def cast_str(string):
    try:
        r = str(string)
    except Exception as _:
        raise ValueError("Can't convert \"{}\" to string".format(string))
    if len(r.strip()) == 0:
        raise ValueError("Arguments can't be empty")

    return r


def cast_int(i):
    try:
        return int(i)
    except Exception as _:
        raise ValueError("Can't convert \"{}\" to int".format(i))


def cast_percent(percent):
    i = ""
    if percent[len(percent) - 1] == "%":
        i = percent[:len(percent) - 1]
    else:
        i = percent
    r = 0.0
    try:
        r = float(i)
    except Exception as _:
        raise ValueError("Can't convert \"{}\" to form float(%)?".format(percent))
    if r > 100.0:
        raise ValueError("Can't have over 100%")
    elif r < 0.0:
        raise ValueError("Can't have less than 0%")

    return r


def cast_big_o(big_o):
    big_o = big_o.replace(" ", "")
    if len(big_o) == 0:
        raise ValueError("Big O can't be empty")
    if len(big_o) < 3:
        return big_o
    if big_o[0].upper() == "O":
        big_o = big_o[1:]
    if big_o[0] == "(" and big_o[len(big_o) - 1] == ")":
        big_o = big_o[1:]
        big_o = big_o[:len(big_o) - 1]

    return big_o


def cast_difficulty(diff):
    if len(diff) == 0:
        raise ValueError("Difficulty can't be empty")
    input_diff = diff
    diff = diff.lower()
    diff = diff[0].upper() + diff[1:]

    if diff == "E":
        diff = "Easy"
    elif diff == "M":
        diff = "Medium"
    elif diff == "H":
        diff = "Hard"

    try:
        a = constants.DIFFICULTY_MULTIPLIER[diff]
    except KeyError as _:
        raise ValueError("Difficulty level \"{}\" not recognised".format(input_diff))
    return diff


def cast_display_name(name):
    if len(name) > constants.MAX_DISPLAY_NAME:
        raise ValueError("Name can't be longer than {} characters".format(constants.MAX_DISPLAY_NAME))
    return cast_str(name)
