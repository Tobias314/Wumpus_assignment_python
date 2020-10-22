from itertools import chain

from model.playfield import Playfield

class KnowledgeBase:

    def __init__(self, playfield_size):
        self.playfield_size = playfield_size
        self.playfield = Playfield(tokens=['B', 'G', 'S', 'P', 'W', 'N', 'V'], size=self.playfield_size)
        for y in range(self.playfield_size):
            for x in range(self.playfield_size):
                self.playfield.set_tokens_at(x, y, ['P', 'W', 'N'])
        self.found_shivers = []
        self.wumpus_found = False

    def add_visited(self, x, y, percepts):
        self.playfield.reset_all_tokens_at(x, y)
        if 'P' not in percepts and 'W' not in percepts:
            percepts.append('N')
        for percept in percepts:
            self.playfield.set_token_at(x, y, percept)
        if ('S' in percepts) and ((x, y) not in self.found_shivers):
            self.found_shivers.append((x, y))
        self.playfield.set_token_at(x, y, 'V') #visited field

    def add_shot_arrow(self, x, y, arrow_direction_x, arrow_direction_y, is_hit):
        assert (abs(arrow_direction_x) + abs(arrow_direction_y)) == 1
        target_position = (x + arrow_direction_x, y + arrow_direction_y)
        if not self.playfield.is_position_in_field(*target_position):
            return
        self.playfield.reset_token_at(target_position[0], target_position[1], 'W')
        neighbors = self.playfield.get_neighbors(target_position[0], target_position[1])
        for n in neighbors:
            self.playfield.reset_token_at(*n, 'S')
        if is_hit:
            self.found_shivers = []
            for a in range(self.playfield_size):
                for b in range(self.playfield_size):
                    self.playfield.reset_token_at(a, b, 'W')
            self.playfield.reset_token_at(*target_position, 'P')
            self.playfield.set_token_at(*target_position, 'N')

    def do_inference(self):
        while self.inference_iteration():
            pass
            #print("inference iteration")

    def visualize_in(self, playfield_widget):
        self.playfield.visualize_in(playfield_widget)

    def inference_iteration(self):
        some_token_changed = False
        for y in range(self.playfield_size):
            for x in range(self.playfield_size):
                if self.infer_neighbors(x,y):
                    #print("infer neighbors true for x:{} y:{}".format(x, y))
                    some_token_changed = True
                if self.check_wumpus(x, y):
                    some_token_changed = True
                    #print("wumpus true for x:{} y:{}".format(x, y))
        return some_token_changed


    def infer_neighbors(self, x, y):
        field_tokens = self.playfield.get_tokens_for(x,y)
        neighbors = self.playfield.get_neighbors(x, y)
        result = False
        if 'S' in field_tokens:
            possible_wumpus_fields = [n for n in neighbors if  'W' in self.playfield.get_tokens_for(*n)]
            if len(possible_wumpus_fields)==1:
                result = (self.playfield.reset_token_at(*possible_wumpus_fields[0], 'P')
                          or self.playfield.reset_token_at(*possible_wumpus_fields[0], 'N'))
        elif 'V' in field_tokens:
            for n in neighbors:
                result = result or self.playfield.reset_token_at(n[0], n[1], 'W')
        if 'V' in field_tokens and 'B' in field_tokens:
            possible_pit_fields = [n for n in neighbors if 'P' in self.playfield.get_tokens_for(*n)]
            if len(possible_pit_fields) == 1:
                result = (self.playfield.reset_token_at(*possible_pit_fields[0], 'W')
                          or self.playfield.reset_token_at(*possible_pit_fields[0], 'N'))
        elif 'V' in field_tokens:
            for n in neighbors:
                result = result or self.playfield.reset_token_at(n[0], n[1], 'P')
        return result

    def check_wumpus(self, x, y):
        if not 'W' in self.playfield.get_tokens_for(x,y):
            return False
        neighbors = self.playfield.get_neighbors(x,y)
        if not all([self.playfield.check_if_neighbors(x,y,x_n,y_n) for (x_n, y_n) in self.found_shivers]):
            self.playfield.reset_token_at(x, y, 'W')
            return True
        return False

    def is_all_save_fields_visited(self):
        for y in range(self.playfield_size):
            for x in range(self.playfield_size):
                tokens = self.playfield.get_tokens_for(x,y)
                if 'V' not in tokens and 'W' not in tokens and 'P' not in tokens:
                    return False
        return True

    def is_field_save(self, x, y):
        tokens = self.playfield.get_tokens_for(x,y)
        if 'W' in tokens or 'P' in tokens:
            return False
        else:
            return True

    def is_field_visited(self, x, y):
        tokens = self.playfield.get_tokens_for(x,y)
        return 'V' in tokens








####old stuff TODO:maybe delete

    #probably deprecated
    def check_shiver(self, x, y):
        if not 'S' in self.playfield.get_tokens_for(x, y):
            return False
        neighbors = self.playfield.get_neighbors(x,y)
        if not any(['W' in self.playfield.get_tokens_for(neighbor[0], neighbor[1]) for neighbor in neighbors]):
            self.playfield.reset_token_at(x, y, 'S')
            return True
        if not all([self.playfield.manhatten_distance(x,y,x_n,y_n)==2 for (x_n, y_n) in self.found_shivers]):
            self.playfield.reset_token_at(x, y, 'S')
            return True
        return False

    #deprecated
    def check_possible_options(self, x, y):
        return self.check_wumpus(x, y)

    # probably deprecated
    def check_pit(self, x, y):
        if not 'P' in self.playfield.get_tokens_for(x, y):
            return False
        neighbors = self.playfield.get_neighbors(x, y)
        if not all(['B' in self.playfield.get_tokens_for(neighbor[0], neighbor[1]) for neighbor in neighbors]):
            self.playfield.reset_token_at(x, y, 'P')
            return True
        return False

    # probably deprecated
    def check_breeze(self, x, y):
        if not 'B' in self.playfield.get_tokens_for(x, y):
            return False
        neighbors = self.playfield.get_neighbors(x, y)
        if not any(['P' in self.playfield.get_tokens_for(neighbor[0], neighbor[1]) for neighbor in neighbors]):
            self.playfield.reset_token_at(x, y, 'B')
            return True
        return False

    #probably deprecated
    def check_save_field(self, x, y):
        if 'N' not in self.playfield.get_tokens_for(x, y):
            return False
        neighbors = self.playfield.get_neighbors(x,y)
        neighbor_tokens = [self.playfield.get_tokens_for(n[0],n[1]) for n in neighbors]
        neighbor_tokens = set(chain.from_iterable([[1, 2, 3], [1, 2], [1, 4, 5, 6, 7]]))
        if not ('W' in neighbor_tokens or 'P' in neighbor_tokens or 'V' not in neighbor_tokens):
            self.playfield.reset_token_at(x, y, 'S')
            return True
        return False
