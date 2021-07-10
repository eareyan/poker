import itertools as it
import pprint
from pathlib import Path
import time

import pandas as pd

from algorithms import psp, compute_schedule_length
from poker import sample_game
from stats import (
    compute_game_stats,
    compute_v_inf,
    compute_v_1_inf,
    compute_bounds,
)


def generate_and_save_game(num_discard_cards, target_epsilon, target_delta):
    # Draw a random game.
    game = sample_game(num_discard_cards=num_discard_cards)

    # Compute the game's stats.
    game_stats = compute_game_stats(game=game)
    v_inf = compute_v_inf(game_stats=game_stats)
    v_1_inf = compute_v_1_inf(game_stats=game_stats)

    # Compute sample complexity and Simulation complexity.
    sample_complexity, simulation_complexity = compute_bounds(
        schedule_length=compute_schedule_length(target_epsilon),
        epsilon=target_epsilon,
        delta=target_delta,
        v_inf=v_inf,
        v_1_inf=v_1_inf,
        game=game,
    )

    pd.DataFrame(
        [
            [
                game["id"],
                game["size_of_game"],
                game["num_discard_cards"],
                game["hand_p1"],
                game["hand_p2"],
                target_epsilon,
                target_delta,
                v_inf,
                v_1_inf,
                sample_complexity,
                simulation_complexity,
            ]
        ]
    ).to_csv("results/games.csv", mode="a", index=False, header=False)

    return game


def psp_run_and_save_stats(game, target_epsilon, target_delta, number_psp_runs):

    # Run PSP multiple times, collect and save stats.
    results = []
    for _ in range(0, number_psp_runs):
        psp_stats = psp(game, target_epsilon, target_delta)
        # pprint.pprint(psp_stats)
        results.append(
            [
                game["id"],
                psp_stats["emp_sample_complexity"],
                psp_stats["emp_simulation_complexity"],
            ]
        )

    # Save results.
    results_df = pd.DataFrame(results)
    results_df.to_csv("results/psp_runs.csv", mode="a", index=False, header=False)


def check_if_results_file_exists():
    if not Path("results/psp_runs.csv").is_file():
        pd.DataFrame(
            [],
            columns=[
                "game_id",
                "size_of_game",
                "num_discard_cards",
                "hand_p1",
                "hand_p2",
                "target_epsilon",
                "target_delta",
                "v_inf",
                "v_1_inf",
                "sample_complexity",
                "simulation_complexity",
            ],
        ).to_csv("results/games.csv", index=False)

    if not Path("results/psp_runs.csv").is_file():
        pd.DataFrame(
            [],
            columns=[
                "game_id",
                "emp_sample_complexity",
                "emp_simulation_complexity",
            ],
        ).to_csv("results/psp_runs.csv", index=False)


if __name__ == "__main__":

    check_if_results_file_exists()

    # Fixed parameters: delta, and the number of psp runs.
    exp_target_delta = 1 / 10 ** 6
    exp_number_psp_runs = 10

    for _, exp_num_discard_cards, exp_target_epsilon in it.product(
        range(10), [1, 2], [0.25, 0.1]
    ):
        t0 = time.time()
        random_game = generate_and_save_game(
            num_discard_cards=exp_num_discard_cards,
            target_epsilon=exp_target_epsilon,
            target_delta=exp_target_delta,
        )
        psp_run_and_save_stats(
            game=random_game,
            target_epsilon=exp_target_epsilon,
            target_delta=exp_target_delta,
            number_psp_runs=exp_number_psp_runs,
        )
        print(
            f"took {time.time() - t0 : .2f} secs to run game with parameters: "
            f"exp_num_discard_cards = {exp_num_discard_cards}, "
            f"exp_target_epsilon = {exp_target_epsilon}"
        )
