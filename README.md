# Take-home Test: The big IMDB quest

This Python package scrapes the [IMDbTop250](https://www.imdb.com/chart/top/?ref_=nv_mv_250)
website for common moovie statistics and then adjust moovie ratings based on
number of votes and number of Oscar award won. Result is exported to a CSV file.


## Usage:


```
# 1., Clone the repository

git clone https://github.com/balintalfoldy/imdb-scaper.git
```


```
# 2., cd into repository

cd imdb-scaper
```


```
# 3-4., Create a virtual env in needed and then activate it

python -m venv venv

venv/Scripts/activate
```

```
# 5., Install required packages

pip install -r requirements.txt
```

```
# 6., Set PATH_TO_CSV in config.yaml
```
```
# 7., Run main.py

python imdb_scraper/main.py
```