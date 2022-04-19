import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget


class MazeDrawer(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.maze = None

    def paintEvent(self, event):
        if not self.maze:
            return
        grid_dim = math.floor(min(self.width(), self.height()) / self.maze.dim)
        self.painter = QPainter()
        self.painter.begin(self)
        for i in range(self.maze.dim):
            for j in range(self.maze.dim):
                if self.maze.grid[i][j] == 0:
                    self.painter.setBrush(Qt.GlobalColor.white)
                elif self.maze.grid[i][j] == 1:
                    self.painter.setBrush(Qt.GlobalColor.black)
                else:
                    self.painter.setBrush(Qt.GlobalColor.cyan)
                self.painter.drawRect(i * grid_dim, j * grid_dim, grid_dim, grid_dim)
        # Start of maze
        self.painter.setBrush(Qt.GlobalColor.green)
        self.painter.drawEllipse(
            (self.maze.start[0] + 0.2) * grid_dim,
            (self.maze.start[1] + 0.2) * grid_dim,
            grid_dim * 0.65,
            grid_dim * 0.65,
        )

        # End of maze
        self.painter.setPen(QPen(Qt.GlobalColor.red, 5))
        self.painter.drawLine(
            (self.maze.end[0] + 0 + 0.2) * grid_dim,
            (self.maze.end[1] + 0 + 0.2) * grid_dim,
            (self.maze.end[0] + 1 - 0.15) * grid_dim,
            (self.maze.end[1] + 1 - 0.15) * grid_dim,
        )
        self.painter.drawLine(
            (self.maze.end[0] + 0 + 0.2) * grid_dim,
            (self.maze.end[1] + 1 - 0.15) * grid_dim,
            (self.maze.end[0] + 1 - 0.15) * grid_dim,
            (self.maze.end[1] + 0 + 0.2) * grid_dim,
        )
        self.painter.end()

    def resize(self, width, height):
        self.setFixedSize(min(width, height), min(width, height))
        self.update()

    def set_maze(self, maze):
        self.maze = maze
        self.update()
