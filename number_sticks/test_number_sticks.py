"""
Test code to solve the number sticks problem.
"""
import pytest

import number_sticks


@pytest.fixture(autouse=True, scope="session")
def before_tests():
    assert number_sticks.FROM_TO_CACHE == {}

    number_sticks.populate_cache()
    yield True

    number_sticks.FROM_TO_CACHE = {}



def test_compute_moves():
    """ """
    assert number_sticks.compute_moves(4, 5) == 3


def test_populate_cache():
    """ """
    number_sticks.FROM_TO_CACHE = {}
    number_sticks.populate_cache()

    assert number_sticks.FROM_TO_CACHE[4][4] == 0
    assert number_sticks.FROM_TO_CACHE[4][5] == 3


def test_generate_numbers():
    gen = number_sticks.generate_numbers(3)

    assert next(gen) == [0, 0, 0]
    assert next(gen) == [0, 0, 1]
    assert next(gen) == [0, 0, 2]


def test_candidate_numbers():
    cands, cand_moves = number_sticks.candidate_numbers(55, 3)

    assert cands[:4] == [55, 56, 59, 65]
    assert cand_moves[65] == 1


def test_find_lowest_sum():
    vals = number_sticks.find_lowest_sum(59, 12, 98)

    assert vals[0] == '86 + 12 = 98, takes 4 moves.'


def test_find_lowest_sub():
    vals = number_sticks.find_lowest_sub(59, 12, 98)

    assert vals[0] == '50 - 12 = 38, takes 4 moves.'
