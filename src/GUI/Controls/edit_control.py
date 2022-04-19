from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class EditControl(QWidget):
    """
    Represents editing controls
    """

    def __init__(self, maze_pressed):
        super().__init__()

        layout = QVBoxLayout()

        self.maze_button = QPushButton("Maze")
        self.maze_button.setFixedSize(100, 30)
        self.maze_button.pressed.connect(maze_pressed)

        layout.addWidget(self.maze_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def resize(self, width, height):
        self.setFixedSize(width, height)
