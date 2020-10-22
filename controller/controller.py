#type checking imports
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.gamestate import GameState
    from model.knowledgebase import KnowledgeBase
    from gui.mainwindow import MainWindow


class Controller:

    def __init__(self, initial_game_state: GameState, knowledge_base: KnowledgeBase, gui: MainWindow):
        self.game_state = initial_game_state
        self.knowledge_base = knowledge_base
        self.gui = gui
        player_position = self.game_state.position
        self.knowledge_base.add_visited(player_position[0], player_position[1], self.game_state.get_current_percepts())
        self.update_knowledge_base()

    def make_step(self):
        raise NotImplementedError

    def turn_right(self):
        self.game_state.turn_right()
        self.update_knowledge_base()

    def turn_left(self):
        self.game_state.turn_left()
        self.update_knowledge_base()

    def move(self, x_direction, y_direction):
        assert abs(x_direction) + abs(y_direction) == 1
        self.game_state.move(x_direction, y_direction)
        player_position = self.game_state.position
        self.knowledge_base.add_visited(player_position[0], player_position[1], self.game_state.get_current_percepts())
        self.update_knowledge_base()

    def move_forward(self):
        self.game_state.move_current_direction()
        player_position = self.game_state.position
        self.knowledge_base.add_visited(player_position[0], player_position[1], self.game_state.get_current_percepts())
        self.update_knowledge_base()

    def on_click_left(self):
        self.move(-1,0)

    def on_click_right(self):
        self.move(1,0)

    def on_click_up(self):
        self.move(0,1)

    def on_click_down(self):
        self.move(0,-1)

    def shoot(self, direction_x, direction_y):
        player_position = self.game_state.position
        is_hit = self.game_state.shoot(direction_x, direction_y)
        if is_hit:
            print("You hit the Wumpus!!!!")
        else:
            print("You missed the Wumpus!!!!")
        self.knowledge_base.add_shot_arrow(player_position[0], player_position[1], direction_x, direction_y, is_hit)
        self.update_knowledge_base()

    def shoot_left(self):
        self.shoot(-1,0)

    def shoot_right(self):
        self.shoot(1,0)

    def shoot_up(self):
        self.shoot(0,1)

    def shoot_down(self):
        self.shoot(0,1)

    def update_knowledge_base(self):
        self.knowledge_base.do_inference()
        self.gui.update_visualization()

