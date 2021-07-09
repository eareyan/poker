import math
import pprint

from poker import sample_game, simulate_game, draw_randomness


def compute_stats(U, V, m, c, delta, T, size_of_game):

    v_hat = (V - (U * U / m)) / (m - 1)

    log_term = math.log(3 * size_of_game * T / delta)

    v_tilde = (
        v_hat
        + (c * c * log_term) / (m - 1)
        + math.sqrt(
            (c * c * log_term / (m - 1)) ** 2 + (2 * c * c * v_hat * log_term / (m - 1))
        )
    )

    eps = min(
        c * math.sqrt(log_term / (2 * m)),
        c * log_term / (3 * m) + math.sqrt(2 * v_tilde * log_term / m),
    )
    return eps


def compute_schedule_length(target_epsilon, c=2.0, beta=2.0):
    return math.ceil(math.log((3.0 * c) / (4.0 * target_epsilon), beta))


def psp(game, target_epsilon, target_delta, c=2.0, beta=2.0):

    # Initialize schedule and other structures.
    T = compute_schedule_length(target_epsilon, c, beta)
    S = len(game["strategy_profiles"].keys())
    alpha = ((2.0 * c) / (3.0 * target_epsilon)) * math.log(
        (3.0 * T * S) / target_delta
    )
    active_set = game["strategy_profiles"].keys()
    stats = {strategy_profile: {"U": 0, "V": 0} for strategy_profile in active_set}
    m = 0

    psp_stats = {
        "stats": stats,
        "schedule": [math.ceil(alpha * (beta ** t)) for t in range(1, T + 1)],
        "active_set_len": [game["size_of_game"]],
        "emp_simulation_complexity": 0,
        "emp_sample_complexity": 0,
        "epsilon_map": {strategy_profile: math.inf for strategy_profile in active_set},
    }

    # Iterate as per the schedule
    for t in range(1, T + 1):

        # Compute number of samples
        m_marginal = math.ceil(alpha * (beta ** t)) - m
        m = math.ceil(alpha * (beta ** t))

        # Record number of samples used - sample complexity
        psp_stats["emp_sample_complexity"] = m

        # Draw randomness. In poker, draw dealer cards.
        random_cards = draw_randomness(game, m_marginal)

        # Simulation complexity: sum of the number of samples processed times the number of strategy profiles that are active
        psp_stats["emp_simulation_complexity"] += m_marginal * len(active_set)

        # Loop through every active strategy profile, s.
        for s in active_set:

            # Simulate game, that is, complete hands and score them.
            total_sum_p1_points, total_sum_p1_points_squared = simulate_game(
                strategy_profile=s,
                game=game,
                list_of_dealer_cards=random_cards,
            )

            # Accumulate stats.
            stats[s]["U"] = stats[s]["U"] + total_sum_p1_points
            stats[s]["V"] = stats[s]["V"] + total_sum_p1_points_squared

            # Compute and store epsilon for this strategy profile.
            psp_stats["epsilon_map"][s] = compute_stats(
                stats[s]["U"],
                stats[s]["V"],
                m,
                c,
                target_delta,
                T,
                game["size_of_game"],
            )
        # Prune well-estimated strategy profiles.
        active_set = {
            strategy_profile
            for strategy_profile in active_set
            if psp_stats["epsilon_map"][strategy_profile] > target_epsilon
        }
        psp_stats["active_set_len"].append(len(active_set))

        # If there are no more active strategy profiles, return
        if len(active_set) == 0:
            return psp_stats

    return psp_stats


if __name__ == "__main__":

    # Draw a game.
    some_game = sample_game(num_discard_cards=1, bet_grid=["*"])

    # Run PSP on the drawn game.
    example_psp_stats = psp(game=some_game, target_epsilon=0.1, target_delta=0.1)
    pprint.pprint(example_psp_stats)
