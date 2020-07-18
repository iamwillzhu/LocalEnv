from snake_state import State
from a_star_search import a_star

import pytest


@pytest.fixture
def initial_state():
    return State(
            body=[{'x': 5, 'y': 7}, {'x': 4, 'y': 7}, {'x': 4, 'y': 8}],
            board_height=11,
            board_width=11)

@pytest.fixture
def one_away():
    return State(
            body=[{'x': 5, 'y': 8}, {'x': 5, 'y': 7}, {'x': 4, 'y': 7}, {'x': 4, 'y': 8}],
            board_height=11,
            board_width=11)

def matrix_to_string(matrix):
    return "\n".join(["".join([str(value) for value in row]) for row in matrix])

class TestAStarSearch:
    
    def test_a_star_search(self, initial_state):
        path = a_star(initial_state)

        print("\n\n".join([matrix_to_string(state.to_hashable_matrix()) for state in path]))
        assert(len(path) == 3)

    def test_a_star_search_one_away(self, one_away):
        path = a_star(one_away)
        assert(len(path) == 2)


