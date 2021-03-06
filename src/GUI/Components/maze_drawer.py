import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QMessageBox, QWidget


class MazeDrawer(QWidget):
    """
    Draws a maze and handles clicking input between the GUI and the stored maze
    Extends QWidget
    """

    def __init__(self):
        """
        Initializes a MazeDrawer
        """
        super().__init__()
        self.maze = None
        self.left_pressed = False
        self.right_pressed = False
        # mode 0 = build
        # mode 1 = play
        self.mode = 0
        self.draw_end_func = None
        self.place_start = False
        self.place_end = False
        self.show()

    def set_draw_end_func(self, func):
        """
        Sets the function that gets called when the player finishes the maze
        Generally intended to end the timer
        @param func: Function to be called when player finishes maze
        """
        self.draw_end_func = func

    def paintEvent(self, event):
        """
        Called when a paint event occurs on the maze drawe through PyQT
        @param event: PyQT event causing the repaint, unused
        """

        # Do nothing if we don't have a maze yet
        if not self.maze:
            return
        # Show the maze start as path if we are playing maze
        if self.mode == 1:
            self.maze.grid[self.maze.start[0]][self.maze.start[1]] = 2
        # Figure out proper dimensions of grid boxes
        self.grid_dim = math.floor(min(self.width(), self.height()) / self.maze.dim)
        # Copy to make it easier to reference
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
        # Circle for start of maze
        self.painter.setBrush(Qt.GlobalColor.green)
        self.painter.drawEllipse(
            (self.maze.start[0] + 0.2) * grid_dim,
            (self.maze.start[1] + 0.2) * grid_dim,
            grid_dim * 0.65,
            grid_dim * 0.65,
        )

        # X for end of maze

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
        """
        Resizes maze drawer
        @param width: New width in pixels
        @param height: New height in pixels
        """
        # It should be a square, so use the minimum of either dimension
        self.setFixedSize(min(width, height), min(width, height))
        self.update()

    def update(self):
        """
        Updates the maze drawer
        """
        super().update()
        self.repaint()

    def set_maze(self, maze):
        """
        Changes the currently loaded maze
        @param maze: Maze to load in
        """
        self.maze = maze
        self.update()

    def mousePressEvent(self, event):
        """
        Handles mouse presses triggered through PyQT
        @param event: PyQT mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            # Left button means either wall in build mode or path in play mode
            self.set_grid(
                event.position().x(), event.position().y(), 1 if self.mode == 0 else 2
            )
            self.left_pressed = True
        elif event.button() == Qt.MouseButton.RightButton:
            # Right button clears in both cases
            self.set_grid(event.position().x(), event.position().y(), 0)
            self.right_pressed = True

    def mouseReleaseEvent(self, event):
        """
        Handles mouse releases triggered through PyQT
        @param event: PyQT mouse release event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_pressed = False
        elif event.button() == Qt.MouseButton.RightButton:
            self.right_pressed = False

    def mouseMoveEvent(self, event):
        """
        Handles mouse movements triggered through PyQT
        @param event: PyQT mouse move event
        """
        # Do the same things as if we were individually clicking on each of the grids
        if self.left_pressed:
            self.set_grid(
                event.position().x(), event.position().y(), 1 if self.mode == 0 else 2
            )
        elif self.right_pressed:
            self.set_grid(event.position().x(), event.position().y(), 0)

    def set_grid(self, x, y, val):
        """
        Sets the grid to a specific value, checking that the value we want
        to set is valid
        @param x: X coordinate of the event, NOT the row/col dimension
        @param y: Y coordinate of the event, NOT the row/col dimension
        @param val: The value we are trying to set
        """
        # Do nothing if maze doesn't exist
        if not self.maze:
            return
        # Figure out which row and col we are at, return if invalid
        row = int(x // self.grid_dim)
        col = int(y // self.grid_dim)
        if row < 0 or row >= self.maze.dim or col < 0 or col >= self.maze.dim:
            return
        # Cannot build on start or end
        if self.mode == 0 and (
            (row, col) == self.maze.end or (row, col) == self.maze.start
        ):
            return
        can_place = True
        # Can't place track on walls in play mode
        if self.mode == 1 and self.maze.grid[row][col] == 1:
            return

        # We're trying to place maze start
        if self.place_start:
            # Only allow on current open boxes
            if self.maze.grid[row][col] == 0:
                self.maze.start = (row, col)
                self.place_start = False
                self.update()
            self.left_pressed = False
            self.right_pressed = False
            return
        # Same procedure for placing maze end
        if self.place_end:
            if self.maze.grid[row][col] == 0:
                self.maze.end = (row, col)
                self.place_end = False
                self.update()
            self.left_pressed = False
            self.right_pressed = False
            return

        # If we're trying to draw a path, make sure it is connected to another path
        # otherwise it is invalid
        if val == 2:
            neighbors = self.maze.get_neighbors(row, col, path=True)
            can_place = False
            for neighbor in neighbors:
                if self.maze.grid[neighbor[0]][neighbor[1]] == 2:
                    can_place = True
                    break
        # Allowed to place
        if can_place:
            self.maze.grid[row][col] = val
            if (row, col) == self.maze.end and self.mode == 1:
                # Check if we have won, if so run callback and win popup
                self.update()
                if self.draw_end_func:
                    self.draw_end_func()
                self.make_popup("You win!")
        self.update()

    def make_popup(self, message):
        """
        Creates a PyQT pop-up window
        @param message: String text we wish to display
        """
        popup = QMessageBox(self)
        popup.setWindowTitle("Alert")
        popup.setText(message)
        ack = popup.exec()
        if ack:
            return
