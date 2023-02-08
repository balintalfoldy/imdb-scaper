import os

import yaml

# Retrieve config parameters from yaml
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(current_dir), "config.yaml")

with open(file_path, "r") as y:
    config = yaml.safe_load(y)

MAX_NUM_MOOVIES = config.get('MAX_NUM_MOOVIES')
PENALTY_DEVIATION = config.get('PENALTY_DEVIATION')
PENALTY_DEDUCTION = config.get('PENALTY_DEDUCTION')
PATH_TO_CSV = config.get('PATH_TO_CSV')
