import uuid

import pandas as pd

from algorithms import psp
from poker import sample_hands, get_deck, create_game
from stats import compute_game_stats, compute_v_inf, compute_v_1_inf


def run_pair_expt(deck, target_eps, target_delta, beta, do_floor):
    # For the same game, estimate num_discard_cards in [2, 3]
    hand_p1, hand_p2 = sample_hands(deck)
    game_id = str(uuid.uuid4())
    results = []
    for num_discard_cards in [2, 3]:
        game = create_game(
            {
                "deck": [
                    card
                    for card in deck
                    if (card not in hand_p1 and card not in hand_p2)
                ],
                "num_discard_cards": num_discard_cards,
                "hand_p1": hand_p1,
                "hand_p2": hand_p2,
                "bet_grid": ["*"],
            }
        )
        # Run PSP
        psp_stats = psp(game, target_eps, target_delta, beta=beta, do_floor=do_floor)

        # Compute the game's stats.
        game_stats = compute_game_stats(game=game, do_floor=do_floor)

        # Collect results
        results.append(
            [
                target_eps,
                target_delta,
                game_id,
                beta,
                do_floor,
                game["size_of_game"],
                num_discard_cards,
                hand_p1,
                hand_p2,
                compute_v_inf(game_stats=game_stats),
                compute_v_1_inf(game_stats=game_stats),
                psp_stats["emp_sample_complexity"],
                psp_stats["emp_simulation_complexity"],
            ]
        )
    results_df = pd.DataFrame(
        results,
        columns=[
            "target_epsilon",
            "target_delta",
            "beta",
            "do_floor",
            "game_id",
            "size_of_game",
            "num_discard_cards",
            "hand_p1",
            "hand_p2",
            "v_inf",
            "v_1_inf",
            "emp_sample_complexity",
            "emp_simulation_complexity",
        ],
    )
    results_df.to_csv(
        f"results/pair_experiment.csv", mode="a", index=False, header=False
    )


if __name__ == "__main__":

    # Fixed parameters: eps, delta, beta, do_floor, and the number of psp runs.
    expt_deck = get_deck()
    exp_target_eps = 0.01
    exp_target_delta = 0.05
    # exp_beta = 1.1
    exp_beta = 1.05
    # exp_do_floor = True
    exp_do_floor = False
    number_of_games = 150

    for i in range(0, number_of_games):
        print(i)
        run_pair_expt(
            deck=expt_deck,
            target_eps=exp_target_eps,
            target_delta=exp_target_delta,
            beta=exp_beta,
            do_floor=exp_do_floor,
        )
