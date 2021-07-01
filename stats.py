from poker import sample_game, simulate_game, draw_randomness
import itertools as it
import pprint


def compute_mean_strategy_profile(strategy_profile, dealer_cards, game):
    """
    Given a game, computes a map as follows:
            {'mean' : mean,
            'variance': variance}
    :param strategy_profile: a strategy profile, valid in the given game.
    :param dealer_cards: a list of cards.
    :param game: a poker game.
    :return: a map that contains the profile statistics, that is, mean and variance.
    """
    total_sum_p1_points, total_sum_p1_points_squared = simulate_game(
        strategy_profile=strategy_profile,
        game=game,
        list_of_dealer_cards=dealer_cards,
    )
    mean = total_sum_p1_points / len(dealer_cards)
    variance = (total_sum_p1_points_squared / len(dealer_cards)) - mean ** 2
    return {"mean": mean, "variance": variance}


def compute_game_stats(game):
    """
    Given a game, computes a map as follows:
        {strategy_profile :
            {'mean' : mean,
            'variance': variance}
        }
    :param game: a poker game.
    :return: a map that contains the game statistics, that is, for each profile, mean and variance.
    """
    dealer_cards_of_game = [
        list(x) for x in it.combinations(game["deck"], game["num_discard_cards"])
    ]
    return {
        sp: compute_mean_strategy_profile(sp, dealer_cards_of_game, game)
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


if __name__ == "__main__":

    # Draw a random game.
    some_game = sample_game(num_discard_cards=2, bet_grid=["*"])
    some_game_stats = compute_game_stats(some_game)

    # Print game stats.
    pprint.pprint(some_game_stats)
    print(compute_v_inf(some_game_stats))
    print(compute_v_1_inf(some_game_stats))
