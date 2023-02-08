
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests
import logging
from bs4 import BeautifulSoup, ResultSet, Tag

### CONSTANTS ###
BASE_URL = "https://www.imdb.com"
URL_TOP250 = "https://www.imdb.com/chart/top/"
HEADERS = {
    "Accept": "text/html",
    "DNT": "1",
    "Connection": "close",
    # Use Firefox or other browser app i.e. not python or else get error
    "User-Agent": "Firefox/66.0"
}

# Configure logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Helper function to requesting


def get_soup(url: str, headers: Optional[Dict] = None) -> BeautifulSoup:
    """
    Makes a GET request to the specified URL and returns a BeautifulSoup object.

    Args:
        url (str): The URL to make the GET request to.
        headers (Optional[Dict]): Request header.

    """
    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.ConnectTimeout as exc:
        print('Server connection timeout. Please retry later.')
        raise exc
    except Exception as exc:
        logging.error('Error during requesting data from remote.')
        raise exc

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
    """
    Class corresponding for imdb top 250 moovies page:
    https://www.imdb.com/chart/top/?ref_=nv_mv_250
    """
    @classmethod
    def get_result(cls, url: str = URL_TOP250) -> ResultSet:
        """
        Get the table data from:
        https://www.imdb.com/chart/top/?ref_=nv_mv_250

        Args:
            url (str, optional): url to site. Defaults to URL_TOP250.

        """
        soup = get_soup(url=url, headers=HEADERS)
        result = soup.find('tbody',  class_="lister-list").find_all('tr')
        return result


class OneMooviePageResult(ImdbPageResult):
    """
    Class corresponding for one moove in imdb, for example:
    https://www.imdb.com/title/tt0111161/
    """
    @classmethod
    def get_result(cls, url: str) -> Tag:
        """
        Get the relevant data for a particular moovie.

        Args:
            url (str, optional): url to site.
        """
        soup = get_soup(url=url, headers=HEADERS)
        result = soup.find("div", attrs={"data-testid": "awards"})
        return result


class ImdbScraper:
    """
    Scraper class containing all functionalities to process moovie data.
    """

    def __init__(self,
                 top250: Top250PageResult = Top250PageResult,
                 one_moovie: OneMooviePageResult = OneMooviePageResult):
        self.top250 = top250
        self.one_moovie = one_moovie

    def get_moovie_stats(self, limit: int = 20) -> List[MoovieStats]:
        """
        Get moovie statistics.

        Args:
            limit (int): Max number of moovies to request.
        """
        top250_results = self.top250.get_result()

        moovies = []
        for i in range(limit):
            rating = self.get_rating(top250_results[i])
            title = self.get_title(top250_results[i])
            nr_rating = self.get_nr_rating(top250_results[i])
            url = self._get_moovie_url(top250_results[i])
            nr_oscars = self.get_nr_oscars(url)
            stat = MoovieStats(rating, nr_rating, nr_oscars, title)
            moovies.append(stat)
        return moovies

    def get_rating(self, moovie: Tag) -> float:
        """
        Retrieve the imdb rating of the moovie..

        Args:
            moovie (Tag): A moovie item.
        """
        ir = moovie.find("span", attrs={"name": "ir"})["data-value"]
        return round(float(ir), 1)

    def get_nr_rating(self, moovie: Tag) -> int:
        """
        Retrieve the number of ratings.

        Args:
            moovie (Tag): A moovie item.
        """
        nv = moovie.find("span", attrs={"name": "nv"})["data-value"]
        return int(nv)

    def get_title(self, moovie: Tag) -> str:
        """
        Retrieve the title of the moovie.

        Args:
            moovie (Tag): A moovie item.
        """
        title = moovie.find("td", class_="titleColumn").a.text
        return title

    def get_nr_oscars(self, url: str) -> int:
        """
        Retrieve number of Oscar wins.

        Args:
            url (str): url of a moovie.
        """
        one_moovie_result = self.one_moovie.get_result(url)
        awards_txt = one_moovie_result.li.a.text

        nr_oscars = self._extract_oscar_wins(text=awards_txt,
                                             pattern=r"Won\s(\d+)\sOscars")
        return int(nr_oscars)

    def _get_moovie_url(self, moovie: Tag, base_url: str = BASE_URL) -> str:
        href = moovie.find("td", class_="titleColumn").a['href']
        return base_url + href

    def _extract_oscar_wins(self, text: str, pattern: str) -> str:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return '0'
