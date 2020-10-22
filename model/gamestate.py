import math

import numpy as np

from model.playfield import Playfield

SMALL_PENALTY = -1
LARGE_PENALTY = -1000
ARROW_PENALTY = -10
GOLD_BONUS = 1000

DIRECTION_SYMBOL_MAP = {
    (1, 0) : 'PR',
    (0, -1) : 'PD',
    (-1, 0) : 'PL',
    (0, 1) : 'PU',
}


class GameState:

    def __init__(self, map: Playfield, initial_x, initial_y):
        self.map = map
        self.position = np.array([initial_x - 1, initial_y - 1])
        self.score = 0
        self.gold_found = False
        self.direction = [1,0]

    def visualize_in(self, playfield_widget):
        self.map.visualize_in(playfield_widget)
        #playfield_widget.highlight_square(self.position[0], self.position[1])
        playfield_widget.set_background_symbol_at(*self.position, DIRECTION_SYMBOL_MAP[tuple(self.direction)])

    def turn_right(self):
        self.direction = (self.direction[1], -self.direction[0])
        self.score += SMALL_PENALTY

    def turn_left(self):
        self.direction = (-self.direction[1], self.direction[0])
        self.score += SMALL_PENALTY

    def move(self, x_movement, y_movement):

        self.position[0] = min(max(self.position[0] + x_movement, 0), self.map.size - 1)
        self.position[1] = min(max(self.position[1] + y_movement, 0), self.map.size - 1)
        self.score += SMALL_PENALTY
        if 'G' in self.map.get_tokens_for(self.position[0], self.position[1]):
            print("Hurray you found the GOLD!!!!")
            self.gold_found = True
            self.score += GOLD_BONUS
        if 'P' in self.map.get_tokens_for(self.position[0], self.position[1]):
            print("You fell in a pit!!!")
            self.score += LARGE_PENALTY
            return
        if 'W' in self.map.get_tokens_for(self.position[0], self.position[1]):
            print("You got eaten by THE WUMPUS!!!")
            self.score += LARGE_PENALTY
            return

    def move_current_direction(self):
        self.move(*self.direction)

    def move_up(self):
        self.move(0, 1)

    def move_down(self):
        self.move(0, -1)

    def move_left(self):
        self.move(-1, 0)

    def move_right(self):
        self.move(1, 0)

    def grab(self):
        self.score += SMALL_PENALTY
        if 'G' in self.map.get_tokens_for(self.position[0], self.position[1]):
            self.score += GOLD_BONUS

    def shoot(self, x_direction, y_direction):
        assert abs(x_direction) + abs(y_direction) == 1
        target_pos = self.position + np.array([x_direction, y_direction])
        self.score += ARROW_PENALTY
        if not self.map.is_position_in_field(*target_pos):
            return False
        if 'W' in self.map.get_tokens_for(target_pos[0], target_pos[1]):
            self.map.reset_token_at(target_pos[0], target_pos[1], 'W')
            neighbors = self.map.get_neighbors(target_pos[0], target_pos[1])
            for n in neighbors:
                self.map.reset_token_at(*n, 'S')
            return True
        else:
            return False



    def get_current_percepts(self):
        return self.map.get_tokens_for(self.position[0], self.position[1])


    def get_player_neighbor_fields(self):
        neighbor_fields = self.map.get_neighbors(*self.position)
        return neighbor_fields