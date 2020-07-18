class State:
    def __init__(self, body, board_height, board_width, cost=0, target=None, parent=None):
        self.body = body
        self.board_height = board_height
        self.board_width = board_width
        self.cost=cost
        self.parent=parent
        self.target=body[-1] if target is None else target

    def __lt__(self, other):
        return self.cost + self.get_heuristic() < other.cost + other.get_heuristic()

    def __repr__(self):
        return "\n".join(["".join([str(value) for value in row]) for row in self.to_hashable_matrix()])

    def __str__(self):
        return "\n".join(["".join([str(value) for value in row]) for row in self.to_hashable_matrix()])


    def to_hashable_matrix(self):
        '''
        method to convert the snake body into a hashable matrix

        Parameters:
        ----------

        Return:
        ------
        output: A 2-d tuple representation of the snake on a board with map_size's dimensions
        '''

        body = list(self.body)
        matrix = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]

        head = body.pop(0)

        matrix[head["y"]][head["x"]] = 2 

        for body_part in body:
            matrix[body_part["y"]][body_part["x"]] = 1

        return tuple(tuple(row) for row in matrix)
    


    def get_successors(self):
        '''
        method to return a list of successor states

        Parameters:
        ----------

        Return:
        ------
        successors: A list of snake bodies/states that are the successors of the current snake state
        '''
        
        matrix = self.to_hashable_matrix()
        successors = []

        for i in range(self.board_height):
            for j in range(self.board_width):
                if matrix[i][j] == 2:
                    if (i > 0 and matrix[i-1][j] == 0) or (i > 0 and self.target["x"] == j and self.target["y"] == i-1):
                        successors.append(
                                State(
                                    body=create_successor_body(self.body, {"x": j, "y": i-1}),
                                    board_height=self.board_height,
                                    board_width=self.board_width,
                                    cost=self.cost + 1,
                                    target=self.target,
                                    parent=self))
                    if (j > 0 and matrix[i][j-1] == 0) or (j > 0 and self.target["x"] == j-1 and self.target["y"] == i):
                        successors.append(
                                State(
                                    body=create_successor_body(self.body, {"x": j-1, "y": i}),
                                    board_height=self.board_height,
                                    board_width=self.board_width,
                                    cost=self.cost + 1,
                                    target=self.target,
                                    parent=self))

                    if (i < self.board_height - 1 and matrix[i+1][j] == 0) or (i < self.board_height - 1 and self.target["x"] == j and self.target["y"] == i+1):
                        successors.append(
                                State(
                                    body=create_successor_body(self.body, {"x": j, "y": i+1}),
                                    board_height=self.board_height,
                                    board_width=self.board_width,
                                    cost=self.cost + 1,
                                    target=self.target,
                                    parent=self))
                    if (j < self.board_width - 1 and matrix[i][j+1] == 0) or (j < self.board_width - 1 and self.target["x"] == j+1 and self.target["y"] == i):
                        successors.append(
                                State(
                                    body=create_successor_body(self.body, {"x": j+1, "y": i}),
                                    board_height=self.board_height,
                                    board_width=self.board_width,
                                    cost=self.cost + 1,
                                    target=self.target,
                                    parent=self))

            #TODO: not really needed but how do you break out of two loops in python?
        return successors

    def get_heuristic(self):
        return abs(self.body[0]["x"] - self.target["x"]) + abs(self.body[0]["y"] - self.target["y"])

    def is_goal(self):
        return self.body[0]["y"] == self.target["y"] and self.body[0]["x"] == self.target["x"]

    def get_path(self):
        current_state = self
        path = []

        while current_state is not None:
            path.append(current_state)
            current_state = current_state.parent

        return tuple(reversed(path))

def create_successor_body(body, new_head_pos):
    successor = list(body)

    successor.pop()
    successor.insert(0, new_head_pos)

    return successor
