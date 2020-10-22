#type checking imports
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.gamestate import GameState
    from model.knowledgebase import KnowledgeBase
    from gui.mainwindow import MainWindow

import random
import math

from controller.controller import Controller

class RuleBasedAi(Controller):

    def __init__(self, initial_game_state: GameState, knowledge_base: KnowledgeBase, gui: MainWindow):
        super().__init__(initial_game_state, knowledge_base, gui)

    def make_decisions(self):
        if self.game_state.gold_found:
            return
        neighbor_fields = [[n,0] for n in self.game_state.get_player_neighbor_fields()]

        #check whether we are next to the wumpus
        wumpus_field = None
        for n in neighbor_fields:
            tokens = self.knowledge_base.playfield.get_tokens_for(*n[0])
            if 'W' in tokens and 'P' not in tokens and 'N' not in tokens:
                wumpus_field = n[0]
        if wumpus_field:
            shoot_direction = (wumpus_field[0] - self.game_state.position[0], wumpus_field[1] - self.game_state.position[1])
            self.shoot(*shoot_direction)
            return

        all_save_fields_visited = self.knowledge_base.is_all_save_fields_visited()
        for i in range(len(neighbor_fields)):
            n = neighbor_fields[i][0]
            n_direction = [n[0]-self.game_state.position[0], n[1]-self.game_state.position[1]]
            diff = [n_direction[0]-self.game_state.direction[0], n_direction[1]-self.game_state.direction[1]]
            neighbor_fields[i][1] += max(abs(diff[0]), abs(diff[1]))
            if self.knowledge_base.is_field_visited(*n):
                neighbor_fields[i][1]+=10
            if self.knowledge_base.is_field_save(*n):
                neighbor_fields[i][1]+=0
            elif 'N' in self.knowledge_base.playfield.get_tokens_for(*n):
                if not all_save_fields_visited:
                    neighbor_fields[i][1]+=100
            else:
                neighbor_fields[i][1]+=1000
        target=[None,math.inf]
        for n in neighbor_fields:
            if n[1] < target[1]:
                target=n

        print("target is ({},{})".format(*target[0]))
        print("penalty is {}".format(target[1]))
        if target[1]%10 == 1:
            t_dir = [target[0][0] - self.game_state.position[0], target[0][1] - self.game_state.position[1]]
            cross_product = self.game_state.direction[0]*t_dir[1] - self.game_state.direction[1]*t_dir[0]
            if cross_product < 0:
                self.turn_right()
            else:
                self.turn_left()
        elif target[1]%10 == 2:
            self.turn_left()
            self.turn_left()

        self.move_forward()

    def make_step(self):
        self.make_decisions()
        return

        if self.game_state.gold_found:
            return
        neighbor_fields = self.game_state.get_player_neighbor_fields()

        #check whether we are next to the wumpus
        wumpus_field = None
        for n in neighbor_fields:
            tokens = self.knowledge_base.playfield.get_tokens_for(*n)
            if 'W' in tokens and 'P' not in tokens and 'N' not in tokens:
                wumpus_field = n
        if wumpus_field:
            shoot_direction = (wumpus_field[0] - self.game_state.position[0], wumpus_field[1] - self.game_state.position[1])
            self.shoot(*shoot_direction)
            return
        #move to the next save undiscovered field or to a random save field, if all save fields are discovered
        #consider also unsafe fields
        save_neighbor_fields = []
        maybe_save_neighbor_fields = []
        unsave_neighbor_fields = []
        for n in neighbor_fields:
            if self.knowledge_base.is_field_save(*n):
                save_neighbor_fields.append(n)
            elif 'N' in self.knowledge_base.playfield.get_tokens_for(*n):
                maybe_save_neighbor_fields.append(n)
            else:
                unsave_neighbor_fields.append(n)
        if self.knowledge_base.is_all_save_fields_visited() and maybe_save_neighbor_fields:
            target = random.choice(maybe_save_neighbor_fields)
        elif save_neighbor_fields:
            target = random.choice(save_neighbor_fields)
        elif maybe_save_neighbor_fields:
            target = random.choice(maybe_save_neighbor_fields)
        else:
            target = random.choice(neighbor_fields)
        move_direction = (target[0]-self.game_state.position[0], target[1]-self.game_state.position[1])
        self.move(*move_direction)




