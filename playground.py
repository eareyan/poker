import pprint

from poker import create_game, get_deck, simulate_game
from tabulate import tabulate

from stats import compute_game_stats, compute_v_inf, compute_v_1_inf

if __name__ == "__main__":

    deck = get_deck()

    hand_p1 = ["H13", "D13", "S13", "H14", "D14"]
    hand_p2 = ["H2", "D3", "S6", "C7", "H10"]

    some_game = create_game(
        {
            "deck": [
                card for card in deck if (card not in hand_p1 and card not in hand_p2)
            ],
            "num_discard_cards": 1,
            "hand_p1": hand_p1,
            "hand_p2": hand_p2,
            "bet_grid": ["*"],
        }
    )
    pprint.pprint(some_game)
    results = []
    for strategy_profile in some_game["strategy_profiles"]:
        for dealer_card in some_game["deck"]:
            total_sum_p1_points, total_sum_p1_points_squared = simulate_game(
                strategy_profile, some_game, [[dealer_card]]
            )
            results.append([strategy_profile, dealer_card, total_sum_p1_points])
    print(
        tabulate(
            results,
            ["strategy_profile", "card", "total_sum_p1_points"],
            tablefmt="grid",
        )
    )
    # Compute the game's stats.
    game_stats = compute_game_stats(game=some_game)
    v_inf = compute_v_inf(game_stats=game_stats)
    v_1_inf = compute_v_1_inf(game_stats=game_stats)
    print(tabulate([[v_inf, v_1_inf]], ["v_inf", "v_1_inf"], tablefmt="grid"))
