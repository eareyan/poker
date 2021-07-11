import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def game_scatter_plot(results, num_discard_cards):
    results_to_plot = results[results["num_discard_cards"] == num_discard_cards]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(f"Results num_discard_cards = {num_discard_cards}")

    x = results_to_plot["v_inf"]
    y = results_to_plot["emp_sample_complexity"]
    print(x.min(), x.max())
    ax1.plot(x, y, "o", color="black")
    ax1.set_title("emp_sample_complexity")
    ax1.set_xlim(0, 1)
    ax1.set_xlabel("v_inf")

    x = results_to_plot["v_1_inf"]
    y = results_to_plot["emp_simulation_complexity"]
    ax2.plot(x, y, "o", color="red")
    ax2.set_title("emp_simulation_complexity")
    # ax2.set_xlim(0, 1)
    ax2.set_xlabel("v_1_inf")

    # plt.show()
    figure = plt.gcf()
    figure.set_size_inches(12, 6)
    plt.savefig(f"plots/num_discard_cards-{num_discard_cards}.png", bbox_inches="tight")


if __name__ == "__main__":
    games = pd.read_csv("results/games.csv")
    psp_runs = pd.read_csv("results/psp_runs.csv")

    exp_results = games.merge(
        psp_runs,
        how="inner",
        left_on="game_id",
        right_on="game_id",
    )
    exp_results.to_csv("results/join.csv", index=None)

    game_scatter_plot(results=exp_results, num_discard_cards=1)
    game_scatter_plot(results=exp_results, num_discard_cards=2)
