from PyQt6.QtWidgets import QHBoxLayout

from src.GUI.Components import maze_drawer
from src.GUI.Controls import edit_control

from .screen import Screen

SIDEBAR_WIDTH = 0.3
MAZE_WIDTH = 0.7
MAZE_HEIGHT = 0.9


class BuildScreen(Screen):
    """
    Main Build Screen, containing the editing sidebar and the maze drawer
    Extends Screen
    """

    def __init__(self):
        """
        Initializes a BuildScreen
        """
        super().__init__()
        self.maze_drawer = maze_drawer.MazeDrawer()
        self.maze_drawer.resize(self.width() * MAZE_WIDTH, MAZE_HEIGHT * self.height())
        self.edit_sidebar = edit_control.EditControl(self.maze_drawer)
        self.edit_sidebar.resize(self.width() * SIDEBAR_WIDTH, self.height())
        layout = QHBoxLayout()
        layout.addWidget(self.edit_sidebar)
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
        self.edit_sidebar.resize(self.width() * SIDEBAR_WIDTH, self.height())
