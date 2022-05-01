from PyQt6.QtWidgets import QHBoxLayout

from src.GUI.Components import maze_drawer
from src.GUI.Controls import edit_control

from .screen import Screen


class BuildScreen(Screen):
    def __init__(self):
        super().__init__()
        self.maze_drawer = maze_drawer.MazeDrawer()
        self.maze_drawer.resize(self.width() * 0.7, 0.9 * self.height())
        self.edit_sidebar = edit_control.EditControl(self.maze_drawer)
        self.edit_sidebar.resize(self.width() * 0.3, self.height())
        layout = QHBoxLayout()
        layout.addWidget(self.edit_sidebar)
        layout.addWidget(self.maze_drawer)
        self.setLayout(layout)
        self.maze = None

    def resize(self, width, height):
        super().resize(width, height)
        self.maze_drawer.resize(self.width() * 0.7, 0.9 * self.height())
        self.edit_sidebar.resize(self.width() * 0.3, self.height())
