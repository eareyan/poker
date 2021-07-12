import functools
import math
import time

import pandas as pd


def get_scores_dict():
    start_time = time.time()
    ranks = pd.read_csv("ranks.zip", compression="zip")
    end_time = time.time()
    print(f"took {end_time - start_time} sec to read dataframe with hands scores")

    start_time = time.time()
    ranks_score_dict = {}
    for row in ranks.itertuples(index=True, name="Pandas"):
        ranks_score_dict[row.hands] = row.value
    end_time = time.time()
    print(f"took {end_time - start_time} to create dict with hands scores")

    return ranks_score_dict


HANDS_RANKS_SCORE_DICT = None


def get_hand_score(hand, do_floor):
    """
    Scores a given hand. Implements a singleton on variable HANDS_RANKS_SCORE_DICT
    so that it is loaded into memory only once.
    :param hand: a hand.
    :param do_floor: floors card scores.
    :return:  the score of the hand.
    """
    global HANDS_RANKS_SCORE_DICT
    if HANDS_RANKS_SCORE_DICT is None:
        HANDS_RANKS_SCORE_DICT = get_scores_dict()
    return (
        HANDS_RANKS_SCORE_DICT[str(hand).replace(",", "")]
        if not do_floor
        else math.floor(HANDS_RANKS_SCORE_DICT[str(hand).replace(",", "")])
    )


def left_hand_points(
    left_hand,
    right_hand,
    do_floor,
):
    if get_hand_score(left_hand, do_floor) > get_hand_score(right_hand, do_floor):
        return 1
    elif get_hand_score(left_hand, do_floor) < get_hand_score(right_hand, do_floor):
        return -1
    else:
        return 0


def compare_cards(x, y, suit_to_number={"H": 0, "S": 1, "C": 2, "D": 3}):
    suit_x, rank_x = x[0], int(x[1:])
    suit_y, rank_y = y[0], int(y[1:])
    assert 2 <= rank_x <= 14 and 2 <= rank_y <= 14
    assert suit_x in suit_to_number.keys() and suit_y in suit_to_number.keys()
    if rank_x > rank_y:
        return 1
    elif rank_x < rank_y:
        return -1
    else:
        return suit_to_number[suit_x] - suit_to_number[suit_y]


def append_cards(initial_hand, new_cards):
    new_hand = initial_hand + new_cards
    new_hand.sort(key=functools.cmp_to_key(compare_cards))
    return new_hand
