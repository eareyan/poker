from unittest import TestCase
from score_hands import append_cards, get_hand_score, left_hand_points
from poker import create_game


class Test(TestCase):
    def test_left_hand_points(self):
        some_left_hand = ["D7", "D11", "D12", "D13", "D14"]
        some_right_hand = ["D10", "D11", "D12", "D13", "D14"]
        assert left_hand_points(some_left_hand, some_right_hand) == -1
        assert left_hand_points(some_right_hand, some_left_hand) == 1
        assert left_hand_points(some_right_hand, some_right_hand) == 0
        assert left_hand_points(some_left_hand, some_left_hand) == 0

    def test_compare_cards(self):

        some_incomplete_hand = ["D7", "C11", "D12"]
        more_cards = ["C4", "S3"]
        new_hand = append_cards(some_incomplete_hand, more_cards)
        assert new_hand == ["S3", "C4", "D7", "C11", "D12"]
        assert 0 < get_hand_score(new_hand) <= 134

        some_incomplete_hand = ["C4", "D2", "S2", "S14"]
        more_cards = ["C3"]
        new_hand = append_cards(some_incomplete_hand, more_cards)
        assert new_hand == ["S2", "D2", "C3", "C4", "S14"]
        assert 0 < get_hand_score(new_hand) <= 134

        some_incomplete_hand = ["H14", "S14"]
        more_cards = ["C3", "D3", "S3"]
        new_hand = append_cards(some_incomplete_hand, more_cards)
        assert new_hand == ["S3", "C3", "D3", "H14", "S14"]
        assert 0 < get_hand_score(new_hand) <= 134

    def test_create_game(self):
        some_game = create_game(
            {
                "deck": None,
                "num_discard_cards": 1,
                "hand_p1": ["H2", "H3", "D3", "C7", "D14"],
                "hand_p2": ["D10", "D11", "D12", "D13", "D14"],
                "bet_grid": [1, 2],
            }
        )
        for s in some_game["strategy_profiles"].values():
            p1_complete_hand = append_cards(s["p1"]["hand"], ["H5"])
            p2_complete_hand = append_cards(s["p2"]["hand"], ["H5"])
            assert 0 < get_hand_score(p1_complete_hand) <= 134
            assert 0 < get_hand_score(p2_complete_hand) <= 134
