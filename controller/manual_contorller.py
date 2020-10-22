#type checking imports
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.gamestate import GameState
    from model.knowledgebase import KnowledgeBase
    from gui.mainwindow import MainWindow

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot

from controller.controller import Controller

class ManualController(Controller):

    def __init__(self, initial_game_state: GameState, knowledge_base: KnowledgeBase, gui: MainWindow):
        super().__init__(initial_game_state, knowledge_base, gui)
        self.controls_widget = QWidget()
        v_layout = QVBoxLayout()
        controls_container = QWidget()
        h_layout = QHBoxLayout()
        button_left = QPushButton('left')
        button_left.clicked.connect(self.on_click_left)
        h_layout.addWidget(button_left)
        button_right = QPushButton('right')
        button_right.clicked.connect(self.on_click_right)
        h_layout.addWidget(button_right)
        button_up = QPushButton('up')
        button_up.clicked.connect(self.on_click_up)
        h_layout.addWidget(button_up)
        button_down = QPushButton('down')
        button_down.clicked.connect(self.on_click_down)
        h_layout.addWidget(button_down)
        button_turn_left = QPushButton('turn_left')
        button_turn_left.clicked.connect(self.turn_left)
        h_layout.addWidget(button_turn_left)
        button_turn_right = QPushButton('turn_right')
        button_turn_right.clicked.connect(self.turn_right)
        h_layout.addWidget(button_turn_right)
        button_move_forward = QPushButton('move_forward')
        button_move_forward.clicked.connect(self.move_forward)
        h_layout.addWidget(button_move_forward)
        controls_container.setLayout(h_layout)
        v_layout.addWidget(controls_container)

        shoot_controls_container = QWidget()
        h_layout2 = QHBoxLayout()
        button_shoot_left = QPushButton('shoot_left')
        button_shoot_left.clicked.connect(self.shoot_left)
        h_layout2.addWidget(button_shoot_left)
        button_shoot_right = QPushButton('shoot_right')
        button_shoot_right.clicked.connect(self.shoot_right)
        h_layout2.addWidget(button_shoot_right)
        button_shoot_up = QPushButton('shoot_up')
        button_shoot_up.clicked.connect(self.shoot_up)
        h_layout2.addWidget(button_shoot_up)
        button_shoot_down = QPushButton('shoot_down')
        button_shoot_down.clicked.connect(self.shoot_down)
        h_layout2.addWidget(button_shoot_down)
        shoot_controls_container.setLayout(h_layout2)
        v_layout.addWidget(shoot_controls_container)

        self.controls_widget.setLayout(v_layout)

    def make_step(self):
        pass