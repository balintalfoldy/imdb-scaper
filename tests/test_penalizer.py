import pytest
from imdb_scraper import penalizer


@pytest.mark.parametrize("nr_rating, max_nr_rating, deviation, deduction, precision, expected", [
    (348253, 2697294, 100000, 0.1, 1, 2.4),
    (766395, 2697294, 100000, 0.1, 1, 2.0),
    (2617280, 2697294, 100000, 0.2, 2, 0.17)
])
def test_penalizer(nr_rating, max_nr_rating, deviation, deduction, precision, expected):
    assert penalizer.penalizer(nr_rating, max_nr_rating, deviation,
                               deduction, precision) == expected


def test_penalizer_fails():
    with pytest.raises(ValueError) as exc:
        penalizer.penalizer(766395, 2697294, 0, 0.1, 1)
