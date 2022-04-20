from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.Maze.maze import Maze


class PlayControl(QWidget):
    """
    Represents play controls
    """

    def __init__(self, maze_drawer):
        super().__init__()

        layout = QVBoxLayout()

        self.maze_drawer = maze_drawer
        self.maze_drawer.mode = 1
        self.maze = self.maze_drawer.maze

        self.load_selected_button = QPushButton("Load Selected Maze")
        self.load_selected_button.pressed.connect(self.load_selected_maze)
        self.load_selected_button.setFixedSize(150, 40)

        self.clear_maze_button = QPushButton("Clear")
        self.clear_maze_button.pressed.connect(self.clear_maze)
        self.clear_maze_button.setFixedSize(150, 40)
        self.clear_maze_button.setEnabled(False)

        self.maze_list = QComboBox()
        self.maze_list.addItems(Maze.saved_mazes.keys())

        self.maze_name_label = QLabel("")

        layout.addWidget(self.maze_list)
        layout.addWidget(self.load_selected_button)
        layout.addWidget(self.maze_name_label)
        layout.addWidget(self.clear_maze_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def update(self):
        Maze.load_saved_mazes()
        self.maze_list.clear()
        self.maze_list.addItems(Maze.saved_mazes.keys())
        if not self.maze:
            return
        self.clear_maze_button.setEnabled(True)
        self.maze_name_label.setText(self.maze.name)
        if self.maze.name in Maze.saved_mazes:
            self.maze_list.setCurrentText(self.maze.name)
        self.maze_drawer.update()

    def load_selected_maze(self):
        if len(Maze.saved_mazes) == 0:
            self.make_popup("No saved mazes!")
        else:
            maze_selected = self.maze_list.currentText()
            self.maze = Maze.get_saved_maze(maze_selected)
            self.maze_changed = False
            self.maze_drawer.set_maze(self.maze)
            self.update()

    def resize(self, width, height):
        self.setFixedSize(width, height)
        self.update()

    def clear_maze(self):
        self.load_selected_maze()

    def make_popup(self, message):
        popup = QMessageBox(self)
        popup.setWindowTitle("Alert")
        popup.setText(message)
        ack = popup.exec()

        if ack:
            return
