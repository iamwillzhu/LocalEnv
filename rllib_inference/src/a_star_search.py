from queue import PriorityQueue

def a_star(initial_state):
    frontier = PriorityQueue()
    explored = set()

    frontier.put((initial_state.cost + initial_state.get_heuristic(), initial_state))
    while not frontier.empty():
        current_state = frontier.get()[1]

        if current_state.to_hashable_matrix() not in explored:
            explored.add(current_state.to_hashable_matrix())

            if current_state.is_goal():
                return current_state.get_path()
            successors = current_state.get_successors()
            for successor in successors:
                frontier.put((successor.cost + successor.get_heuristic(), successor))

    raise Exception("No solution found")
