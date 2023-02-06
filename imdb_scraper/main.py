import pandas as pd
from scraper import ImdbScraper
from penalizer import penalizer
from oscar import oscar_calculator
from pathlib import Path

MAX_NUM_MOOVIES = 20
PENALTY_DEVIATION = 100000
PENALTY_DEDUCTION = 0.1


def run(path_to_csv: str):
    # Extract top moovies statisticss
    scraper = ImdbScraper()
    moovies_stats = scraper.get_moovie_stats(MAX_NUM_MOOVIES)

    # Convert result to pandas df for easier calculations
    moovies_stats_df = pd.DataFrame(moovies_stats)

    # Penalize ratings based on number of ratings
    max_nr_rating = moovies_stats_df['nr_rating'].max()
    moovies_stats_df['rating_penalty'] = moovies_stats_df.apply(
        lambda row: penalizer(
            nr_rating=row['nr_rating'],
            max_nr_rating=max_nr_rating,
            deviation=PENALTY_DEVIATION,
            deduction=PENALTY_DEDUCTION,
            precision=1), axis=1)

    # Reward ratings based on number of oscars won
    moovies_stats_df['oscars_reward'] = moovies_stats_df.apply(
        lambda row: oscar_calculator(nr_oscars=row['nr_oscars']), axis=1)

    # Calculate adjusted rating
    moovies_stats_df['adjusted_rating'] = (moovies_stats_df['rating']
                                           - moovies_stats_df['rating_penalty']
                                           + moovies_stats_df['oscars_reward'])

    # Save the result to csv
    path_to_csv = Path(path_to_csv)
    moovies_stats_df.to_csv(path_to_csv)
