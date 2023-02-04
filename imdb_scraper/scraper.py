# Import packages
from bs4 import BeautifulSoup
import requests
from typings import Dict

### CONSTANTS ###

URL = "https://www.imdb.com/chart/top/" # IMDB top 250 moovie list url
MAX_NUM_MOOVIES = 20 # Number of desired moovies from the list

def get_top_moovies_url(doc: BeautifulSoup, limit: int = MAX_NUM_MOOVIES) -> Dict:
    pass

def _get_doc(url: str) -> BeautifulSoup:
    """
    Request the url and parse as a html document.

    Args:
        url (str): The url to the site to be parsed.
    """
    try:
        result = requests.get(url)
    except Exception as exc:
        raise exc

    doc = BeautifulSoup(result.text, "html.parser")
    return doc

table = doc.find('table',  attrs={"data-caller-name": "chart-top250movie"})

# Get the table content by tbody tag
tbody = table.tbody

# Get the relevant column by class name
trs = tbody.find_all(class_="titleColumn")

moovies = {}
# Loop through the contents row by row and extract relevant information
for td in trs:
    rank, info = td.contents[0:2]
    rk = rank.string
    href = info['href']
    ttl = info.text
    moovies[rk] = {'title': ttl, 'url': href}

# print(moovies)
# print(td)
# print(type(td))
