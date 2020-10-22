import math

import numpy as np


def load_playfields_from_txt(file_path):
    idx = 0
    playfields = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if(line[0]=="#"):
                continue
            elif(line[:3]=="NEW"):
                field_size = int(line.split(' ')[1])
                playfields.append(Playfield(size=field_size))
            elif(line[:3]=="END"):
                idx+=1
            else:
                (token_name, x, y) = line.split(' ')
                playfields[-1].set_token_at(int(x) - 1, int(y) - 1, token_name)

    return playfields


def augment_shiver_and_breeze(playfield):
    for y in range(playfield.size):
        for x in range(playfield.size):
            if 'P' in playfield.get_tokens_for(x,y):
                playfield.apply_to_neighbors(x, y, lambda n_x, n_y: playfield.set_token_at(n_x, n_y, 'B'))
            if 'W' in playfield.get_tokens_for(x,y):
                playfield.apply_to_neighbors(x, y, lambda n_x, n_y: playfield.set_token_at(n_x, n_y, 'S'))
    return playfield



class Playfield:

    def __init__(self, tokens=['B', 'G', 'P', 'S', 'W'], size=4):
        self.size = size
        self.tokens_dict = {}
        for i, token in enumerate(tokens):
            self.tokens_dict[token] = i
        self.inverse_tokens_dict = {v: k for k, v in self.tokens_dict.items()}
        self.fields = np.zeros((size, size, len(tokens)))


    def set_token_at(self, x, y, token_name):
        self.fields[y, x, self.tokens_dict[token_name]] = 1

    def set_tokens_at(self, x, y, token_names):
        for token_name in token_names:
            self.set_token_at(x, y, token_name)

    def reset_token_at(self, x, y, token_name):
        old=self.fields[y, x, self.tokens_dict[token_name]] > 0
        self.fields[y, x, self.tokens_dict[token_name]] = 0
        return old

    def reset_tokens_at(self, x, y, token_names):
        for token_name in token_names:
            self.reset_token_at(x, y, token_name)

    def reset_all_tokens_at(self, x, y):
        for token_name in self.tokens_dict.keys():
            self.reset_token_at(x, y, token_name)

    def is_token_set(self, x, y, token_name):
        return self.fields[y, x, self.tokens_dict[token_name]] > 0

    def get_tokens_for(self, x, y):
        indices = np.argwhere(self.fields[y, x] > 0).flatten()
        token_names = [self.inverse_tokens_dict[i] for i in indices]
        return token_names

    def visualize_in(self, playfield_widget):
        for y in range(self.size):
            for x in range(self.size):
                indices = np.argwhere(self.fields[y, x] > 0).flatten()
                token_names = [self.inverse_tokens_dict[i] for i in indices]
                playfield_widget.set_symbols_at(x, y, token_names)

    def get_neighbors(self, x, y):
        neighbors = []
        if x - 1 >= 0:
            neighbors.append((x - 1,y))
        if x + 1 < self.size:
            neighbors.append((x + 1, y))
        if y - 1 >= 0:
            neighbors.append((x, y - 1))
        if y + 1 < self.size:
            neighbors.append((x, y + 1))
        return neighbors

    def apply_to_neighbors(self, x, y, function):
        for n in self.get_neighbors(x, y):
            function(*n)

    def manhatten_distance(self, x1, y1, x2, y2):
        return abs(x2-x1) + abs(y2-y1)

    def check_if_neighbors(self, x1, y1, x2, y2):
        return self.manhatten_distance(x1,y1,x2,y2) == 1

    def is_position_in_field(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size



