# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# or in the "license" file accompanying this file. This file is distributed 
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
# express or implied. See the License for the specific language governing 
# permissions and limitations under the License.

import numpy as np
import random
from .a_star_search import a_star
from .snake_state import State

class MyBattlesnakeHeuristics:
    '''
    The BattlesnakeHeuristics class allows you to define handcrafted rules of the snake.
    '''
    FOOD_INDEX = 0
    def __init__(self):
        pass

    def tail_chase(self, json):
        your_snake_body = json["you"]["body"]
        i, j = your_snake_body[0]["y"], your_snake_body[0]["x"]

        if len(your_snake_body) < 3:
            return None,None

        path = a_star(initial_state=State(
            body=your_snake_body,
            board_height=json["board"]["height"],
            board_width=json["board"]["width"]))

        next_move = path[1].body[0]

        tail_direction = None
        if next_move["y"] == i - 1:
            tail_direction = 0
        if next_move["y"] == i + 1:
            tail_direction = 1
        if next_move["x"] == j - 1:
            tail_direction = 2
        if next_move["x"] == j + 1:
            tail_direction = 3
        return next_move, tail_direction



    
    def go_to_food_if_close(self, state, json):
        '''
        Example heuristic to move towards food if it's close to you.
        '''
        # Get the position of the snake head
        your_snake_body = json["you"]["body"]
        i, j = your_snake_body[0]["y"], your_snake_body[0]["x"]
        
        # Set food_direction towards food
        food = state[:, :, self.FOOD_INDEX]
        
        # Note that there is a -1 border around state so i = i + 1, j = j + 1
        if -1 in state:
            i, j = i+1, j+1
        
        food_direction = None
        if food[i-1, j] == 1:
            food_direction = 0 # up
        if food[i+1, j] == 1:
            food_direction = 1 # down
        if food[i, j-1] == 1:
            food_direction = 2 # left
        if food[i, j+1] == 1:
            food_direction = 3 # right
        return food_direction
    
    def run(self, state, snake_id, turn_count, health, json, action):
        '''
        The main function of the heuristics.
        
        Parameters:
        -----------
        `state`: np.array of size (map_size[0]+2, map_size[1]+2, 1+number_of_snakes)
        Provides the current observation of the gym.
        Your target snake is state[:, :, snake_id+1]
    
        `snake_id`: int
        Indicates the id where id \in [0...number_of_snakes]
    
        `turn_count`: int
        Indicates the number of elapsed turns
    
        `health`: dict
        Indicates the health of all snakes in the form of {int: snake_id: int:health}
        
        `json`: dict
        Provides the same information as above, in the same format as the battlesnake engine.

        `action`: np.array of size 4
        The qvalues of the actions calculated. The 4 values correspond to [up, down, left, right]
        '''
        log_string = ""
        # The default `best_action` to take is the one that provides has the largest Q value.
        # If you think of something else, you can edit how `best_action` is calculated
        best_action = int(np.argmax(action))
                
        if health[snake_id] > 70:
            next_move,tail_direction = self.tail_chase(json)
            if next_move is not None:
                best_action = tail_direction if tail_direction is not None else best_action
                log_string = f"{next_move}, {tail_direction}"

        # Example heuristics to eat food that you are close to.
        if health[snake_id] < 30:
            food_direction = self.go_to_food_if_close(state, json)
            if food_direction:
                best_action = food_direction
                log_string = "Went to food if close."
                

        # TO DO, add your own heuristics
        
        assert best_action in [0, 1, 2, 3], "{} is not a valid action.".format(best_action)
        return best_action, log_string
