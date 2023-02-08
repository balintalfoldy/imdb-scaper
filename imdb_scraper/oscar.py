
REWARD_MAPPER = {  # number of oscars: reward point
    0: 0.0,
    1: 0.3,
    2: 0.3,
    3: 0.5,
    4: 0.5,
    5: 0.5,
    6: 1.0,
    7: 1.0,
    8: 1.0,
    9: 1.0,
    10: 1.0,
    11: 1.5,
}


def oscar_calculator(nr_oscars: int) -> float:
    """
    Calculate reward based on number of Oscars.

    Args:
        nr_oscars (int): The number of Oscars the moovie has won.

    """
    return REWARD_MAPPER.get(nr_oscars, REWARD_MAPPER.get(11))  # if 10+ default to 11
