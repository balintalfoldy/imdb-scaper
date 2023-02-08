import pytest
from imdb_scraper.scraper import Top250PageResult, OneMooviePageResult, ImdbScraper
from unittest.mock import patch
import unittest.mock as mock
from bs4 import BeautifulSoup

# Get testing data for one moovie
with open("tests/onemoovieresult.html", "r", encoding='utf-8') as file:
    onemoovie_txt = file.read()
onemoovie_bs = BeautifulSoup(onemoovie_txt, "html.parser")
onemoovie_result = onemoovie_bs.find("div", attrs={"data-testid": "awards"})

# Get testing data for the top 250 moovies
with open("tests/top250result.html", "r", encoding='utf-8') as file:
    top250_txt = file.read()
top250_bs = BeautifulSoup(top250_txt, "html.parser")
top250_result = top250_bs.find('tbody',  class_="lister-list").find_all('tr')


@pytest.fixture
def imdb():
    return ImdbScraper(Top250PageResult, OneMooviePageResult)


@pytest.fixture
def moovie():
    return top250_result[0]


def test_top250_page_result():
    with mock.patch('imdb_scraper.scraper.get_soup', return_value=top250_bs):
        assert Top250PageResult().get_result() == top250_result


def test_onemoovie_page_result():
    with mock.patch('imdb_scraper.scraper.get_soup', return_value=onemoovie_bs):
        assert OneMooviePageResult().get_result(
            url='some_url') == onemoovie_result


def test_get_rating(moovie, imdb):
    assert imdb.get_rating(moovie) == 9.2


def test_get_nr_rating(moovie, imdb):
    assert imdb.get_nr_rating(moovie) == 2697712


def test_get_title(moovie, imdb):
    assert imdb.get_title(moovie) == "A remény rabjai"


def test_get_moovie_url(imdb, moovie, base_url="https://www.imdb.com"):
    assert imdb._get_moovie_url(
        moovie, base_url) == "https://www.imdb.com/title/tt0111161/"


@pytest.mark.parametrize("text, pattern, expected", [
    ("Won 4 Oscars", r"Won\s(\d+)\sOscars", "4"),
    ("Nominated for 2 Oscars", r"Won\s(\d+)\sOscars", "0")])
def test_extract_oscar_wins(text, pattern, expected, imdb):
    assert imdb._extract_oscar_wins(text, pattern) == expected


def test_get_nr_oscars(imdb, url="https://www.imdb.com/title/tt0111161/"):
    with mock.patch('imdb_scraper.scraper.OneMooviePageResult.get_result', return_value=onemoovie_result):
        assert imdb.get_nr_oscars(url) == 0
