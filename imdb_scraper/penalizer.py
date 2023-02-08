
import math


def penalizer(nr_rating: int, max_nr_rating: int,
              deviation: int, deduction: float, precision: int) -> float:
    """
    Calculate penalty based on number of ratings.

    Args:
        nr_rating (int): Number of ratings.
        max_nr_rating (int): The maximum number of ratings i.e. benchmark.
        deviation (int): The deviation used in the calculation of the penalty.
        deduction (float): The deduction used in the calculation of the penalty.
        precision (int): The precision used for rounding the final result.

    """
    try:
        penalty = (max_nr_rating - nr_rating) / deviation * deduction
    except ZeroDivisionError as exc:
        raise ValueError("Invalid values for deviation or deduction "
                         "- results in division by zero.") from exc

    return math.ceil(penalty * 10**precision) / 10**precision
