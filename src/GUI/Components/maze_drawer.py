import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QMessageBox, QWidget


class MazeDrawer(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.maze = None
        self.left_pressed = False
        self.right_pressed = False
        # mode 0 = build
        # mode 1 = play
        self.mode = 0
        self.draw_end_func = None
        self.place_start = False
        self.place_end = False

    def set_draw_end_func(self, func):
        self.draw_end_func = func

    def paintEvent(self, event):
        if not self.maze:
            return
        if self.mode == 1:
            self.maze.grid[self.maze.start[0]][self.maze.start[1]] = 2
        self.grid_dim = math.floor(min(self.width(), self.height()) / self.maze.dim)
        grid_dim = self.grid_dim
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

        # Pen width 5 looks good for a 20x20 maze
        # Scale the width down as the dimension increases
        pen_width = 5 * (20 / self.maze.dim)
        self.painter.setPen(QPen(Qt.GlobalColor.red, pen_width))
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_grid(
                event.position().x(), event.position().y(), 1 if self.mode == 0 else 2
            )
            self.left_pressed = True
        elif event.button() == Qt.MouseButton.RightButton:
            self.set_grid(event.position().x(), event.position().y(), 0)
            self.right_pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_pressed = False
        elif event.button() == Qt.MouseButton.RightButton:
            self.right_pressed = False

    def mouseMoveEvent(self, event):
        if self.left_pressed:
            self.set_grid(
                event.position().x(), event.position().y(), 1 if self.mode == 0 else 2
            )
        elif self.right_pressed:
            self.set_grid(event.position().x(), event.position().y(), 0)

    def set_grid(self, x, y, val):
        if not self.maze:
            return
        row = int(x // self.grid_dim)
        col = int(y // self.grid_dim)
        if row < 0 or row >= self.maze.dim or col < 0 or col >= self.maze.dim:
            return
        if self.mode == 0 and (
            (row, col) == self.maze.end or (row, col) == self.maze.start
        ):
            return
        can_place = True
        if self.mode == 1 and self.maze.grid[row][col] == 1:
            return

        if self.place_start:
            if self.maze.grid[row][col] == 0:
                self.maze.start = (row, col)
                self.place_start = False
                self.update()
            self.left_pressed = False
            self.right_pressed = False
            return

        if self.place_end:
            if self.maze.grid[row][col] == 0:
                self.maze.end = (row, col)
                self.place_end = False
                self.update()
            self.left_pressed = False
            self.right_pressed = False
            return

        if val == 2:
            neighbors = self.maze.get_neighbors(row, col)
            can_place = False
            for neighbor in neighbors:
                if self.maze.grid[neighbor[0]][neighbor[1]] == 2:
                    can_place = True
                    break
        if can_place:
            self.maze.grid[row][col] = val
            if (row, col) == self.maze.end and self.mode == 1:
                self.update()
                if self.draw_end_func:
                    self.draw_end_func()
                self.make_popup("You win!")
        self.update()

    def make_popup(self, message):
        popup = QMessageBox(self)
        popup.setWindowTitle("Alert")
        popup.setText(message)
        ack = popup.exec()

        if ack:
            return
