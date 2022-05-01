from PyQt6.QtWidgets import QHBoxLayout

from src.GUI.Components import maze_drawer
from src.GUI.Controls import play_control

from .screen import Screen

SIDEBAR_WIDTH = 0.3
MAZE_WIDTH = 0.7
MAZE_HEIGHT = 0.9


class PlayScreen(Screen):
    """
    Play screen for playing mazes
    Has a play controls sidebar and the maze drawer
    Extends Screen
    """

    def __init__(self):
        """
        Initializes a PlayScreen
        """
        super().__init__()
        self.maze_drawer = maze_drawer.MazeDrawer()
        self.maze_drawer.resize(self.width() * MAZE_WIDTH, MAZE_HEIGHT * self.height())
        self.play_sidebar = play_control.PlayControl(self.maze_drawer)
        self.play_sidebar.resize(self.width() * SIDEBAR_WIDTH, self.height())
        layout = QHBoxLayout()
        layout.addWidget(self.play_sidebar)
        layout.addWidget(self.maze_drawer)
        self.setLayout(layout)
        self.maze = None

    def resize(self, width, height):
        """
        Resize the screen
        Calls base class to resize the window and then sets internal widget size
        @param width: new width in pixels
        @param height: new height in pixels
        """
        super().resize(width, height)
        self.maze_drawer.resize(self.width() * MAZE_WIDTH, MAZE_HEIGHT * self.height())
        self.play_sidebar.resize(self.width() * SIDEBAR_WIDTH, self.height())
