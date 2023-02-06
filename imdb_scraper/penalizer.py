
import math


def penalizer(rating: float, nr_rating: int, max_nr_rating: int,
              deviation: int, deduction: float) -> float:
    try:
        decimal_index = str(rating).index('.')
        precision = len(str(rating)) - decimal_index - 1
    except ValueError:
        precision = 1

    new_rating = rating - (max_nr_rating - nr_rating) / deviation * deduction
    return math.ceil(new_rating * 10**precision) / 10**precision
