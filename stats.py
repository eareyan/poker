import math

from poker import sample_game, simulate_game
import itertools as it
import pprint


def compute_strategy_profile_stats(strategy_profile, dealer_cards, game, do_floor):
    """
    Given a game, computes a map as follows:
            {'mean' : mean,
            'variance': variance}
    :param strategy_profile: a strategy profile, valid in the given game.
    :param dealer_cards: a list of cards.
    :param game: a poker game.
    :param do_floor:
    :return: a map that contains the profile statistics, that is, mean and variance.
    """
    total_sum_p1_points, total_sum_p1_points_squared = simulate_game(
        strategy_profile=strategy_profile,
        game=game,
        list_of_dealer_cards=dealer_cards,
        do_floor=do_floor,
    )
    mean = total_sum_p1_points / len(dealer_cards)
    variance = (total_sum_p1_points_squared / len(dealer_cards)) - mean ** 2
    return {"mean": mean, "variance": variance}


def compute_game_stats(game, do_floor):
    """
    Given a game, computes a map as follows:
        {strategy_profile :
            {'mean' : mean,
            'variance': variance}
        }
    :param game: a poker game.
    :param do_floor:
    :return: a map that contains the game statistics, that is, for each profile, mean and variance.
    """
    dealer_cards_of_game = [
        list(x) for x in it.combinations(game["deck"], game["num_discard_cards"])
    ]
    return {
        sp: compute_strategy_profile_stats(sp, dealer_cards_of_game, game, do_floor)
        for sp in game["strategy_profiles"].keys()
    }


def compute_v_inf(game_stats):
    """
    Computes the v_inf norm of a game, defined as max_{s \in S, p \in P} v_p(s).
    Since this game is zero-sum, the variances are the same for each player, hence,
        max_{s \in S, p \in P} v_p(s) = max_{s \in S} v_p(s)
    :param game_stats: a dictionary as follows:
        {strategy_profile :
            {'mean' : mean,
            'variance': variance}
        }
    :return: the v_inf norm of a game
    """
    return max([stats["variance"] for stats in game_stats.values()])


def compute_v_1_inf(game_stats):
    """
    Computes the v_1_inf norm of a game, defined as sum_{s \in S} max_{p \in P} v_p(s).
    Since this game is zero-sum, the variances are the same for each player, hence,
        sum_{s \in S} max_{p \in P} v_p(s) = sum_{s \in S} v_p(s)
    :param game_stats: a dictionary as follows:
        {strategy_profile :
            {'mean' : mean,
            'variance': variance}
        }
    :return: the v_1_inf norm of a game
    """
    return sum([stats["variance"] for stats in game_stats.values()])


def compute_sample_complexity(
    schedule_length, epsilon, delta, v_inf, game, c=2, beta=2
):
    return 2 + math.ceil(
        2
        * beta
        * math.log(3 * schedule_length * game["size_of_game"] / delta)
        * (2 * c / epsilon + v_inf / epsilon ** 2)
    )


def compute_simulation_complexity(
    schedule_length, epsilon, delta, v_1_inf, game, c=2, beta=2
):
    return 2 + math.ceil(
        2
        * beta
        * math.log(3 * schedule_length * game["size_of_game"] / delta)
        * (2 * c * game["size_of_game"] / (2 / 2 * epsilon) + v_1_inf / epsilon ** 2)
    )


def compute_bounds(schedule_length, epsilon, delta, v_inf, v_1_inf, game, c=2, beta=2):
    return (
        compute_sample_complexity(
            schedule_length, epsilon, delta, v_inf, game, c, beta
        ),
        compute_simulation_complexity(
            schedule_length, epsilon, delta, v_1_inf, game, c, beta
        ),
    )


if __name__ == "__main__":

    # Draw a random game.
    some_game = sample_game(
        num_discard_cards=2,
    )
    some_game_stats = compute_game_stats(some_game, do_floor=False)

    # Print game stats.
    pprint.pprint(some_game_stats)
    print(compute_v_inf(some_game_stats))
    print(compute_v_1_inf(some_game_stats))
