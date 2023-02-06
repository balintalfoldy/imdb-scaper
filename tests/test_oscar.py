import pytest
from imdb_scraper import oscar


@pytest.mark.parametrize("nr_oscars, expected", [
    (3, 0.5),
    (14, 1.5),
    (0, 0.0)
])
def test_penalizer(nr_oscars, expected):
    assert oscar.oscar_calculator(nr_oscars) == expected
