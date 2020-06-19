import numpy as np

from expanseanalyzer.common.constants import REFERENCES_DIR


def norm_to_one(array: np.array) -> np.array:
    """
    Norms all values of a numpy array to one.

    Do not confuse with normalize!

    :param array: numpy array
    :return: normed numpy array
    """
    array /= array.max()

    return array


def multiply_and_round(num: float, factor: float = 100, precision: int = 2) -> float:
    """
    Takes a floating point value (presumably one between 0 and 1), multiplies it with a given factor (default 100)
    and rounds it with the given precision.

    :param num: number to multiply and round
    :param factor: multiplying factor (default = 100, to create percentages)
    :param precision: rounding precision
    :return: product rounded with precision
    """
    return round(num * factor, precision)


def dist(item: "tuple of int") -> int:
    """
    Calculates the absolute distance between the two int values of a tuple.

    :param item: tuple of ints
    :return: absolute distance between tuple elements
    """
    return abs(item[0] - item[1])


def stopwords():
    """
    Loads all stopwords from the stopwords file into a set.
    """
    words = set(open(REFERENCES_DIR / 'stopwords.txt', 'r').read().splitlines())
    return words.union([w.replace("'", '’') for w in words])


STOPWORDS = stopwords()
