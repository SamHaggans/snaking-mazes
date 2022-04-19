from PyQt6.QtWidgets import QHBoxLayout

from src.GUI.Components import maze_drawer
from src.GUI.Controls import edit_control
from src.Maze.maze import Maze

from .screen import Screen


class BuildScreen(Screen):
    def __init__(self):
        super().__init__()
        self.maze_drawer = maze_drawer.MazeDrawer()
        self.maze_drawer.resize(self.width() * 0.8, 0.9 * self.height())
        self.edit_sidebar = edit_control.EditControl(self.bt_press)
        self.edit_sidebar.resize(self.width() * 0.2, self.height())
        layout = QHBoxLayout()
        layout.addWidget(self.edit_sidebar)
        layout.addWidget(self.maze_drawer)
        self.setLayout(layout)
        self.maze = None
        self.mazes = [Maze("test", 10, 1), Maze("test", 15, 1), Maze("test", 20, 1)]
        self.id = -1

    def set_maze(self, maze):
        self.maze = maze
        self.maze_drawer.set_maze(maze)

    def bt_press(self):
        self.id += 1
        self.maze = self.mazes[self.id % 3]
        self.set_maze(self.maze)

    def resize(self, width, height):
        self.setFixedSize(width, height)
        self.maze_drawer.resize(self.width() * 0.8, 0.9 * self.height())
        self.edit_sidebar.resize(self.width() * 0.2, self.height())
