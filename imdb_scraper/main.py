import os
import logging
from pathlib import Path

import pandas as pd
import yaml
from config import (MAX_NUM_MOOVIES, PATH_TO_CSV, PENALTY_DEDUCTION,
                    PENALTY_DEVIATION)
from oscar import oscar_calculator
from penalizer import penalizer
from scraper import ImdbScraper


def run():

    # Configure logging
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    # Extract top moovies statisticss
    scraper = ImdbScraper()
    logging.info('Getting moovies stats...')
    moovies_stats = scraper.get_moovie_stats(MAX_NUM_MOOVIES)
    logging.info('Successfully retrieved moovies stats...')

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
    path_to_csv = Path(PATH_TO_CSV)
    moovies_stats_df.to_csv(path_to_csv, encoding='utf-8')
    logging.info('Finished processing.')
    print()
    print(f'Result is at {str(path_to_csv)}')


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        logging.error('Processing was unsuccessful.')
        raise exc
