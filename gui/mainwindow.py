import time

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, QTimer

from gui.playfieldwidget import PlayfieldWidget
from model.playfield import load_playfields_from_txt, augment_shiver_and_breeze
from model.gamestate import GameState
from model.knowledgebase import KnowledgeBase
from controller.manual_contorller import ManualController
from controller.rulebasedai import RuleBasedAi

PLAYFIELD_SIZE = 4

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Wumpus")

        playfields = load_playfields_from_txt("maps.txt")
        playfields = [augment_shiver_and_breeze(playfield) for playfield in playfields]
        playfield = playfields[2]
        self.game_state = GameState(playfield, 1, 1)
        self.knowledge_base = KnowledgeBase(PLAYFIELD_SIZE)

        self.hud_widget = QWidget()
        hud_layout = QHBoxLayout()
        score_label = QLabel("score:")
        hud_layout.addWidget(score_label)
        self.score_widget = QLabel("0")
        hud_layout.addWidget(self.score_widget)
        self.hud_widget.setLayout(hud_layout)

        self.playfield_widget = PlayfieldWidget(PLAYFIELD_SIZE, "gfx/all/")
        self.game_state.visualize_in(self.playfield_widget)
        self.knowledge_base_widget = PlayfieldWidget(PLAYFIELD_SIZE, "gfx/all/")
        self.knowledge_base.visualize_in(self.knowledge_base_widget)

        self.playfields_container = QWidget()
        playfields_layout = QHBoxLayout()
        playfields_layout.addWidget(self.playfield_widget)
        playfields_layout.addWidget(self.knowledge_base_widget)
        self.playfields_container.setLayout(playfields_layout)

        #self.controller = ManualController(self.game_state, self.knowledge_base, self)
        self.controller = RuleBasedAi(self.game_state, self.knowledge_base, self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.controller.make_step)
        self.timer.start(1000)
        #controller_thread = ControllerThread(self.controller)
        #controller_thread.start()
        #controller_thread.run()

        container = QWidget()
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.hud_widget)
        #vertical_layout.addWidget(self.controller.controls_widget)
        vertical_layout.addWidget(self.playfields_container)
        container.setLayout(vertical_layout)
        self.setCentralWidget(container)

    def update_visualization(self):
        self.game_state.visualize_in(self.playfield_widget)
        self.knowledge_base.visualize_in(self.knowledge_base_widget)
        self.score_widget.setText(str(self.game_state.score))


class ControllerThread(QThread):
    def __init__(self, controller):
        QThread.__init__(self)
        self.controller = controller

    def run(self):
        while True:
            self.controller.make_step()
            #time.sleep(1)
            self.sleep(0.5)

