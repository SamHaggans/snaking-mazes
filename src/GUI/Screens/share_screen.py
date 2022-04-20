import pickle

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from src.Maze.maze import Maze

from .screen import Screen


class ShareScreen(Screen):
    def __init__(self):
        super().__init__()

        self.file_dialog = QFileDialog()
        layout = QVBoxLayout()

        self.save_selected_button = QPushButton("Save Selected Maze to New File")
        self.save_selected_button.pressed.connect(self.save_selected_maze)
        self.save_selected_button.setFixedHeight(40)
        self.save_selected_button.setMaximumWidth(self.width() * 0.8)

        self.maze_list = QComboBox()
        self.maze_list.addItems(Maze.saved_mazes.keys())
        self.maze_list.setMaximumWidth(self.width() * 0.8)

        self.import_button = QPushButton("Import Maze File to Library")
        self.import_button.pressed.connect(self.import_maze)
        self.import_button.setFixedHeight(40)
        self.import_button.setMaximumWidth(self.width() * 0.8)

        self.save_selected_button.setMinimumWidth(self.width() * 0.4)
        self.maze_list.setMinimumWidth(self.width() * 0.4)
        self.import_button.setMinimumWidth(self.width() * 0.4)

        layout.addWidget(self.maze_list)
        layout.addWidget(self.save_selected_button)
        layout.addWidget(self.import_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def import_maze(self):
        chosen_file = QFileDialog.getOpenFileName(self, filter="Maze Files (*.maze)")
        if chosen_file:
            try:
                with open(chosen_file[0], "rb") as file:
                    read_maze = pickle.load(file)
                    read_maze.save_to_file()
                    Maze.load_saved_mazes()
                    self.update()
                    self.make_popup("Successfully Loaded File!")
            except Exception:
                self.make_popup("Something went wrong processing that file.")

    def save_selected_maze(self):
        if len(Maze.saved_mazes) == 0:
            self.make_popup("No saved mazes!")
            return
        maze_selected = self.maze_list.currentText()
        maze = Maze.get_saved_maze(maze_selected)
        chosen_file = QFileDialog.getSaveFileName(self, filter="Maze Files (*.maze)")
        if chosen_file:
            try:
                maze.save_to_file(filename=chosen_file[0])
                self.make_popup(f"Maze saved to {chosen_file[0]}")
            except Exception:
                self.make_popup("Something went wrong saving that file.")

    def resize(self, width, height):
        self.setFixedSize(width, height)
        self.update()

    def update(
        self,
    ):
        Maze.load_saved_mazes()
        self.maze_list.clear()
        self.maze_list.addItems(Maze.saved_mazes.keys())
        self.save_selected_button.setMaximumWidth(self.width() * 0.8)
        self.maze_list.setMaximumWidth(self.width() * 0.8)
        self.import_button.setMaximumWidth(self.width() * 0.8)
        self.save_selected_button.setMinimumWidth(self.width() * 0.4)
        self.maze_list.setMinimumWidth(self.width() * 0.4)
        self.import_button.setMinimumWidth(self.width() * 0.4)

    def make_popup(self, message):
        popup = QMessageBox(self)
        popup.setWindowTitle("Alert")
        popup.setText(message)
        ack = popup.exec()

        if ack:
            return
