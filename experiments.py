import pprint
import pandas as pd

from algorithms import psp, compute_schedule_length
from poker import sample_game
from stats import (
    compute_game_stats,
    compute_v_inf,
    compute_v_1_inf,
    compute_bounds,
)

if __name__ == "__main__":
    # Parameters
    target_epsilon = 0.25
    target_delta = 0.1

    # Draw a random game.
    game = sample_game(num_discard_cards=2)

    # Compute the game's stats.
    game_stats = compute_game_stats(game)
    v_inf = compute_v_inf(game_stats)
    v_1_inf = compute_v_1_inf(game_stats)

    # Compute sample complexity and Simulation complexity.
    sample_complexity, simulation_complexity = compute_bounds(
        schedule_length=compute_schedule_length(target_epsilon),
        epsilon=target_epsilon,
        delta=target_delta,
        v_inf=v_inf,
        v_1_inf=v_1_inf,
        game=game,
    )

    # Run PSP multiple times, collect stats.
    results = []
    for _ in range(0, 10):
        psp_stats = psp(game, target_epsilon, target_delta)
        pprint.pprint(psp_stats)
        results.append(
            [
                v_inf,
                v_1_inf,
                sample_complexity,
                simulation_complexity,
                psp_stats["final_m"],
            ]
        )

    # Save results.
    results_df = pd.DataFrame(
        results,
        columns=[
            "v_inf",
            "v_1_inf",
            "sample_complexity",
            "simulation_complexity",
            "final_m",
        ],
    )
    results_df.to_csv("results/test.csv", index=False)