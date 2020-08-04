from constants import DIFFICULTY_MULTIPLIER

''' CASTING FUNCS '''


def cast_str(string):
    r = ""
    try:
        r = str(string)
    except Exception as _:
        raise ValueError("Can't convert {} to string".format(string))
    return r


def cast_int(i):
    r = 0
    try:
        r = int(i)
    except Exception as _:
        raise ValueError("Can't convert {} to int".format(i))
    return r


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
        raise ValueError("Can't convert {} to form float(%)?".format(percent))
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

    diff = diff.lower()
    diff = diff[0].upper() + diff[1:]
    try:
        a = DIFFICULTY_MULTIPLIER[diff]
    except KeyError as _:
        raise ValueError("Difficulty level: {} not recognised".format(diff))
    return diff
