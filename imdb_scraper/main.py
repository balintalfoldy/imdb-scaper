import pandas as pd
from scraper import ImdbScraper
from penalizer import penalizer

MAX_NUM_MOOVIES = 20
PENALTY_DEVIATION = 100000
PENALTY_DEDUCTION = 0.1


def run():
    # Extract top moovies statistics
    scraper = ImdbScraper()
    moovies_stats = scraper.get_moovie_stats(MAX_NUM_MOOVIES)

    # Convert result to pandas df for easier calculations
    moovies_stats_df = pd.DataFrame(moovies_stats)

    # Penalize ratings
    max_nr_rating = moovies_stats_df['nr_rating'].max()
    moovies_stats_df['rating_adjusted'] = moovies_stats_df.apply(
        lambda row: penalizer(rating=row['rating'],
                              nr_rating=row['nr_rating'],
                              max_nr_rating=row['max_nr_rating'],
                              deviation=PENALTY_DEVIATION,
                              deduction=PENALTY_DEDUCTION), axis=1)
