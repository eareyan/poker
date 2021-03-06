import time
from pathlib import Path

import pandas as pd

from algorithms import psp, compute_schedule_length
from poker import *
from stats import (
    compute_game_stats,
    compute_v_inf,
    compute_v_1_inf,
    compute_bounds,
)


def generate_and_save_game(
    num_discard_cards, target_epsilon, target_delta, beta, do_floor
):
    # Draw a random game.
    game = sample_game(num_discard_cards=num_discard_cards)
    # game = generate_rigged_game()

    # Compute the game's stats.
    game_stats = compute_game_stats(game=game, do_floor=do_floor)
    v_inf = compute_v_inf(game_stats=game_stats)
    v_1_inf = compute_v_1_inf(game_stats=game_stats)

    # Compute sample complexity and Simulation complexity.
    sample_complexity, simulation_complexity = compute_bounds(
        schedule_length=compute_schedule_length(target_epsilon, beta=beta),
        epsilon=target_epsilon,
        delta=target_delta,
        v_inf=v_inf,
        v_1_inf=v_1_inf,
        game=game,
        beta=beta,
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
    ).to_csv(f"results/games_do_floor_{do_floor}.csv", mode="a", index=False, header=False)

    return game


def psp_run_and_save_stats(
    game, target_epsilon, target_delta, number_psp_runs, beta, do_floor
):

    # Run PSP multiple times, collect and save stats.
    results = []
    for _ in range(0, number_psp_runs):
        psp_stats = psp(
            game, target_epsilon, target_delta, beta=beta, do_floor=do_floor
        )
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
    results_df.to_csv(f"results/psp_runs_do_floor_{do_floor}.csv", mode="a", index=False, header=False)


def check_if_results_file_exists(do_floor):
    if not Path(f"results/games_do_floor_{do_floor}.csv").is_file():
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
        ).to_csv(f"results/games_do_floor_{do_floor}.csv", index=False)

    if not Path(f"results/psp_runs_do_floor_{do_floor}.csv").is_file():
        pd.DataFrame(
            [],
            columns=[
                "game_id",
                "emp_sample_complexity",
                "emp_simulation_complexity",
            ],
        ).to_csv(f"results/psp_runs_do_floor_{do_floor}.csv", index=False)


if __name__ == "__main__":

    # Fixed parameters: delta, and the number of psp runs.
    exp_target_delta = 0.05
    exp_number_psp_runs = 1
    number_of_games = 150
    exp_target_eps_grid = [0.01]
    exp_num_discard_cards_grid = [3]
    exp_do_floor = False

    # beta = 2
    # beta = 1.25
    exp_beta = 1.1
    # beta = 1.05

    check_if_results_file_exists(exp_do_floor)

    for _, exp_num_discard_cards, exp_target_epsilon in it.product(
        range(number_of_games), exp_num_discard_cards_grid, exp_target_eps_grid
    ):
        t0 = time.time()
        random_game = generate_and_save_game(
            num_discard_cards=exp_num_discard_cards,
            target_epsilon=exp_target_epsilon,
            target_delta=exp_target_delta,
            beta=exp_beta,
            do_floor=exp_do_floor,
        )
        psp_run_and_save_stats(
            game=random_game,
            target_epsilon=exp_target_epsilon,
            target_delta=exp_target_delta,
            number_psp_runs=exp_number_psp_runs,
            beta=exp_beta,
            do_floor=exp_do_floor,
        )
        print(
            f"took {time.time() - t0 : .2f} secs to run game with parameters: "
            f"exp_num_discard_cards = {exp_num_discard_cards}, "
            f"exp_target_epsilon = {exp_target_epsilon}"
        )
