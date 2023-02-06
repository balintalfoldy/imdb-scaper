
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup, ResultSet

### CONSTANTS ###
BASE_URL = "https://www.imdb.com"  # IMDB url
URL_TOP250 = "https://www.imdb.com/chart/top/"  # IMDB top 250 moovie list url
HEADERS = {
    "Accept": "text/html",
    "DNT": "1",
    "Connection": "close",
    "User-Agent": "Firefox/66.0"
}

# Helper function to requesting


def get_soup(url: str, headers: Optional[Dict] = None) -> BeautifulSoup:
    """
    Makes a GET request to the specified URL and returns a BeautifulSoup object.

    Args:
        url (str): The URL to make the GET request to.
        headers (Optional[Dict]): Request header.

    Returns:
        BeautifulSoup: The BeautifulSoup object created from the response
            of the GET request.

    Raises:
        requests.exceptions.HTTPError: If the GET request returns
            an unsuccessful HTTP status code (status code >= 400).
    """
    request = requests.get(url, headers=headers)
    request.raise_for_status()

    return BeautifulSoup(request.text, "html.parser")

# Data structure for moovie statistics


@dataclass
class MoovieStats:
    rating: float
    nr_rating: int
    nr_oscars: int
    title: str


class ImdbPageResult(ABC):
    """Abstract interface for the content of IMDB pages."""

    @abstractmethod
    def get_result(self, url: str) -> List:
        """Get relevant information."""


class Top250PageResult(ImdbPageResult):

    def get_result(self, url: str = URL_TOP250) -> List:
        soup = get_soup(url=url, headers=HEADERS)
        result = soup.find('tbody',  class_="lister-list").find_all('tr')
        return result


class OneMooviePageResult(ImdbPageResult):

    def get_result(self, url: str) -> List:
        soup = get_soup(url=url, headers=HEADERS)
        result = soup.find("div", attrs={"data-testid": "awards"})
        return result


class ImdbScraper:

    def __init__(self,
                 top250: Top250PageResult = Top250PageResult(),
                 one_moovie: OneMooviePageResult = OneMooviePageResult()):
        self.top250 = top250
        self.one_moovie = one_moovie
        self.top250_results = top250.get_result()

    def get_moovie_stats(self, limit: int = 20) -> List[MoovieStats]:
        moovies = []
        for i in range(limit):
            rating = self.get_rating(i)
            title = self.get_title(i)
            nr_rating = self.get_nr_rating(i)
            nr_oscars = self.get_nr_oscars(i)
            stat = MoovieStats(rating, nr_rating, nr_oscars, title)
            moovies.append(stat)
        return moovies

    def get_rating(self, index: int) -> float:
        moovie = self.top250_results[index]
        ir = moovie.find("span", attrs={"name": "ir"})["data-value"]
        return round(float(ir), 1)

    def get_nr_rating(self, index: int) -> int:
        moovie = self.top250_results[index]
        nv = moovie.find("span", attrs={"name": "nv"})["data-value"]
        return int(nv)

    def get_title(self, index: int) -> str:
        moovie = self.top250_results[index]
        title = moovie.find("td", class_="titleColumn").a.text
        return title

    def get_nr_oscars(self, index: int) -> int:
        url = self._get_moovie_url(index)
        one_moovie_result = self.one_moovie.get_result(url)
        awards_txt = one_moovie_result.li.a.text

        nr_oscars = self._extract_oscar_wins(text=awards_txt,
                                             pattern=r"Won\s(\d+)\sOscars")
        return int(nr_oscars)

    def _get_moovie_url(self, index: int, base_url: str = BASE_URL) -> str:
        moovie = self.top250_results[index]
        href = moovie.find("td", class_="titleColumn").a['href']
        return base_url + href

    def _extract_oscar_wins(self, text: str, pattern: str) -> str:
        """Extracts number of Oscar wins from text.

        Args:
            text (str): The input text to extract from.
            pattern (str): The regular expression pattern to use for extraction.

        """
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return '0'
