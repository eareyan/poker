import itertools as it
import random

from score_hands import append_cards, left_hand_points
from math import comb


def create_game(game_parameters):
    """
    Given game parameters, returns a dictionary that specifies a game.
    :param game_parameters: a dictionary with the following data:
            "deck": a list of cars,
            "num_discard_cards": an integer indicating how many cars players are required to discard,
            "hand_p1": a list of cards,
            "hand_p2": a list of cards,
            "bet_grid": a list of two integers, each integer denoting the bet of each player.
    :return: a dictionary.
    """
    return {
        "deck": game_parameters["deck"],
        "num_discard_cards": game_parameters["num_discard_cards"],
        "hand_p1": game_parameters["hand_p1"],
        "hand_p2": game_parameters["hand_p2"],
        "size_of_game": comb(5, game_parameters["num_discard_cards"])
        * comb(5, game_parameters["num_discard_cards"])
        * len(game_parameters["bet_grid"])
        * len(game_parameters["bet_grid"]),
        "strategy_profiles": {
            (p1_index_discard, p1_bet, p2_index_discard, p2_bet): {
                "p1": {
                    "hand": [
                        c
                        for i, c in enumerate(game_parameters["hand_p1"])
                        if i not in p1_index_discard
                    ],
                    "estimates": (0.0, 0.0),
                },
                "p2": {
                    "hand": [
                        c
                        for i, c in enumerate(game_parameters["hand_p2"])
                        if i not in p2_index_discard
                    ],
                    "estimates": (0.0, 0.0),
                },
            }
            for p1_index_discard, p1_bet, p2_index_discard, p2_bet in it.product(
                it.combinations(range(5), game_parameters["num_discard_cards"]),
                game_parameters["bet_grid"],
                it.combinations(range(5), game_parameters["num_discard_cards"]),
                game_parameters["bet_grid"],
            )
        },
    }


def draw_randomness(game, m):
    """
    Draw a list with m random cards.
    :param game: a poker game.
    :param m: how many samples.
    :return: list of cards.
    """
    return [random.sample(game["deck"], game["num_discard_cards"]) for _ in range(m)]


def simulate_game(strategy_profile, game, list_of_dealer_cards):
    """
    Given a strategy profile, a game, and a list of dealer cards, this function scores the strategy profile for each
    card and return the sum of the scores and the sum of scores squares. Note that we assume a zero-sum game so that
    the sum of scores are for only one player (the negation being the sum of scores for the other), and the sum of
    squares is the same for both players.
    :param strategy_profile: a strategy profile.
    :param game: a poker game.
    :param list_of_dealer_cards: a list with cards.
    :return: sum of scores and sum of scores squared.
    """
    data = game["strategy_profiles"][strategy_profile]
    total_sum_p1_points = 0
    total_sum_p1_points_squared = 0
    for dealer_cards in list_of_dealer_cards:
        p1_complete_hand = append_cards(data["p1"]["hand"], dealer_cards)
        p2_complete_hand = append_cards(data["p2"]["hand"], dealer_cards)
        p1_points = left_hand_points(p1_complete_hand, p2_complete_hand)
        total_sum_p1_points += p1_points
        total_sum_p1_points_squared += p1_points ** 2

    return total_sum_p1_points, total_sum_p1_points_squared


def sample_hands(deck):
    """
    Given a deck, that is, a list of cards, return a random pair of hands.
    :param deck: a list of cards.
    :return: a tuple of hands.
    """
    hands = random.sample(deck, 10)
    return append_cards(hands[:5], []), append_cards(hands[5:], [])


def get_deck():
    """
    Computes a list of cards corresponding to a standard deck.
    :return: a list of cards.
    """
    return [
        f"{card[0]}{card[1]}"
        for card in list(it.product(["H", "S", "C", "D"], range(2, 15)))
    ]


def sample_game(num_discard_cards, bet_grid):
    """
    Samples a random game.
    :param num_discard_cards: an integer encoding how many cards each player must discard.
    :param bet_grid: a list of two integers, each encoding the best of each player.
    :return: a poker game.
    """
    deck = get_deck()
    hand_p1, hand_p2 = sample_hands(deck)
    # hand_p1, hand_p2 = ["H2", "C2", "H4", "C4", "D11"], ["S2", "D2", "S4", "D4", "D12"]

    deck = [card for card in deck if (card not in hand_p1 and card not in hand_p2)]
    return create_game(
        {
            "deck": deck,
            "num_discard_cards": num_discard_cards,
            "hand_p1": hand_p1,
            "hand_p2": hand_p2,
            "bet_grid": bet_grid,
        }
    )
