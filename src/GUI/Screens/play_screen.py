from PyQt6.QtWidgets import QHBoxLayout

from src.GUI.Components import maze_drawer
from src.GUI.Controls import play_control

from .screen import Screen


class PlayScreen(Screen):
    def __init__(self):
        super().__init__()
        self.maze_drawer = maze_drawer.MazeDrawer()
        self.maze_drawer.resize(self.width() * 0.8, 0.9 * self.height())
        self.play_sidebar = play_control.PlayControl(self.maze_drawer)
        self.play_sidebar.resize(self.width() * 0.2, self.height())
        layout = QHBoxLayout()
        layout.addWidget(self.play_sidebar)
        layout.addWidget(self.maze_drawer)
        self.setLayout(layout)
        self.maze = None

    def resize(self, width, height):
        self.setFixedSize(width, height)
        self.maze_drawer.resize(self.width() * 0.8, 0.9 * self.height())
        self.play_sidebar.resize(self.width() * 0.2, self.height())
