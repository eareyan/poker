import math

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

from algorithms import compute_schedule_length
from stats import compute_sample_complexity, compute_simulation_complexity

# TODO: Parameters of experiments: this is probably bad practice and needs to be refactored.
exp_target_delta = 0.05
exp_target_eps = 0.01
beta = 1.1
c = 2


# Copy paste from https://stackoverflow.com/questions/25750170/show-decimal-places-and-scientific-notation-on-the-axis-of-a-matplotlib-plot
class MathTextSciFormatter(mtick.Formatter):
    def __init__(self, fmt="%1.2e"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        decimal_point = "."
        positive_sign = "+"
        tup = s.split("e")
        significand = tup[0].rstrip(decimal_point)
        sign = tup[1][0].replace(positive_sign, "")
        exponent = tup[1][1:].lstrip("0")
        if exponent:
            exponent = "10^{%s%s}" % (sign, exponent)
        if significand and exponent:
            s = r"%s{\times}%s" % (significand, exponent)
        else:
            s = r"%s%s" % (significand, exponent)
        return "${}$".format(s)


def compute_sample_asymptotic_bounds(num_discard_cards):
    size_of_game = 100 if num_discard_cards == 2 else 25
    v_inf_resolution_grid = [i * 0.01 for i in range(0, 110)]
    v_1_inf_resolution_grid = [i for i in range(0, size_of_game + 10)]

    v_inf_asymptotic = [
        (v_inf / exp_target_eps ** 2) * math.log(size_of_game / exp_target_delta)
        for v_inf in v_inf_resolution_grid
    ]

    v_1_inf_asymptotic = [
        (v_1_inf / exp_target_eps ** 2) * math.log(size_of_game / exp_target_delta)
        for v_1_inf in v_1_inf_resolution_grid
    ]

    return {
        "v_inf_asymptotic": {"x": v_inf_resolution_grid, "y": v_inf_asymptotic},
        "v_1_inf_asymptotic": {"x": v_1_inf_resolution_grid, "y": v_1_inf_asymptotic},
    }


def bounds_line(num_discard_cards):
    schedule_length = compute_schedule_length(target_epsilon=exp_target_eps, beta=beta)
    size_of_game = 100 if num_discard_cards == 2 else 25
    v_inf_resolution_grid = [i * 0.01 for i in range(0, 100)]
    v_1_inf_resolution_grid = [i for i in range(0, size_of_game)]

    v_inf_grid = [
        compute_sample_complexity(
            schedule_length=schedule_length,
            epsilon=exp_target_eps,
            delta=exp_target_delta,
            v_inf=v_inf,
            game={"size_of_game": size_of_game},
            c=c,
            beta=beta,
        )
        for v_inf in v_inf_resolution_grid
    ]

    v_1_inf_grid = [
        compute_simulation_complexity(
            schedule_length=schedule_length,
            epsilon=exp_target_eps,
            delta=exp_target_delta,
            v_1_inf=v_1_inf,
            game={"size_of_game": size_of_game},
            c=c,
            beta=beta,
        )
        for v_1_inf in v_1_inf_resolution_grid
    ]

    return {
        "v_inf_grid": {"x": v_inf_resolution_grid, "y": v_inf_grid},
        "v_1_inf_grid": {"x": v_1_inf_resolution_grid, "y": v_1_inf_grid},
    }


def plot_empirical_qtts(
    num_discard_cards,
    results_to_plot,
    ax1,
    ax2,
    marker_shape,
    markersize,
    dot_transparency,
    colors,
):
    # Scatter plot for Empirical sample complexity
    x = results_to_plot["v_inf"]
    y = results_to_plot["emp_sample_complexity"]
    ax1.plot(
        x,
        y,
        marker_shape,
        color=colors["emp_sample_complexity"],
        markersize=markersize,
        alpha=dot_transparency,
    )
    ax1.set_title("Empirical sample complexity")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0)
    ax1.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))
    ax1.set_xlabel(r"$||v||_{\infty}$")

    # Scatter plot for Empirical simulation complexity
    x = results_to_plot["v_1_inf"]
    y = results_to_plot["emp_simulation_complexity"]
    ax2.plot(
        x,
        y,
        marker_shape,
        color=colors["emp_simulation_complexity"],
        markersize=markersize,
        alpha=dot_transparency,
    )
    ax2.set_title("Empirical query complexity")
    ax2.set_xlim(0, 100 if num_discard_cards == 2 else 25)
    ax2.set_ylim(0)
    ax2.yaxis.set_major_formatter(MathTextSciFormatter("%1.2e"))

    ax2.set_xlabel(r"$||v||_{1,\infty}$")


def plot_bounds(num_discard_cards, ax1, ax2):
    # Plot bounds
    bounds = bounds_line(num_discard_cards=num_discard_cards)
    ax1.plot(bounds["v_inf_grid"]["x"], bounds["v_inf_grid"]["y"], "-", color="black")
    ax2.plot(
        bounds["v_1_inf_grid"]["x"], bounds["v_1_inf_grid"]["y"], "-", color="black"
    )
    asymptotic_bounds = compute_sample_asymptotic_bounds(
        num_discard_cards=num_discard_cards
    )
    # a = min(bounds["v_inf_grid"]["y"])
    # b = max(bounds["v_inf_grid"]["y"])
    # ax1.set_yticks(range(a, b, int((b - a) / 5)))
    ax1.plot(
        asymptotic_bounds["v_inf_asymptotic"]["x"],
        asymptotic_bounds["v_inf_asymptotic"]["y"],
        "--",
        color="black",
    )
    ax2.plot(
        asymptotic_bounds["v_1_inf_asymptotic"]["x"],
        asymptotic_bounds["v_1_inf_asymptotic"]["y"],
        "--",
        color="black",
    )


def plot_and_save(num_discard_cards):
    # Plot and save figure.
    figure = plt.gcf()
    figure.set_size_inches(4, 8)
    plt.tight_layout()
    plt.savefig(
        f"plots/num_discard_cards_{num_discard_cards}.png",
        bbox_inches="tight",
        transparent=True
    )


def get_data(exp_do_floor):
    # Read results
    games = pd.read_csv(f"results/games_do_floor_{exp_do_floor}.csv")
    psp_runs = pd.read_csv(f"results/psp_runs_do_floor_{exp_do_floor}.csv")

    exp_results = games.merge(
        psp_runs,
        how="inner",
        left_on="game_id",
        right_on="game_id",
    )
    exp_results.to_csv(f"results/join_do_floor_{exp_do_floor}.csv", index=None)
    return exp_results


if __name__ == "__main__":

    # Read Data
    do_floor = get_data(exp_do_floor=True)
    no_floor = get_data(exp_do_floor=False)

    # Parameters
    exp_num_discard_cards = 1

    # Plot results, side-by-side.
    exp_fig, (exp_ax1, exp_ax2) = plt.subplots(2, 1)

    # Set plot title.
    exp_fig.suptitle(
        f"Players discard {exp_num_discard_cards} "
        f"card{'' if exp_num_discard_cards == 1 else 's'}."
    )

    plot_empirical_qtts(
        num_discard_cards=exp_num_discard_cards,
        results_to_plot=do_floor[
            do_floor["num_discard_cards"] == exp_num_discard_cards
        ],
        ax1=exp_ax1,
        ax2=exp_ax2,
        marker_shape=".",
        markersize=3.5,
        dot_transparency=0.5,
        colors={"emp_sample_complexity": "red", "emp_simulation_complexity": "red"},
    )

    plot_empirical_qtts(
        num_discard_cards=exp_num_discard_cards,
        results_to_plot=no_floor[
            no_floor["num_discard_cards"] == exp_num_discard_cards
        ],
        ax1=exp_ax1,
        ax2=exp_ax2,
        marker_shape=".",
        markersize=3.5,
        dot_transparency=0.5,
        colors={"emp_sample_complexity": "blue", "emp_simulation_complexity": "blue"},
    )

    plot_bounds(num_discard_cards=exp_num_discard_cards, ax1=exp_ax1, ax2=exp_ax2)
    plot_and_save(num_discard_cards=exp_num_discard_cards)
