import itertools as it
import random

from score_hands import append_cards, left_hand_points
from math import comb


def create_game(game_parameters):
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
    return [random.sample(game["deck"], game["num_discard_cards"]) for _ in range(m)]


def simulate_game(strategy_profile, game, random_cards):
    data = game["strategy_profiles"][strategy_profile]
    total_sum_p1_points = 0
    total_sum_p1_points_squared = 0
    for dealer_cards in random_cards:
        p1_complete_hand = append_cards(data["p1"]["hand"], dealer_cards)
        p2_complete_hand = append_cards(data["p2"]["hand"], dealer_cards)
        p1_points = left_hand_points(p1_complete_hand, p2_complete_hand)
        total_sum_p1_points += p1_points
        total_sum_p1_points_squared += p1_points ** 2

    return total_sum_p1_points, total_sum_p1_points_squared


def sample_hands(deck):
    hands = random.sample(deck, 10)
    return append_cards(hands[:5], []), append_cards(hands[5:], [])


def get_deck():
    return [
        f"{card[0]}{card[1]}"
        for card in list(it.product(["H", "S", "C", "D"], range(2, 15)))
    ]


def sample_game(num_discard_cards, bet_grid):
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
