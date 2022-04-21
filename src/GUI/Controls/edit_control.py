from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDial,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.Maze.maze import Maze


class EditControl(QWidget):
    """
    Represents editing controls
    """

    def __init__(self, maze_drawer):
        super().__init__()
        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_choice = 0

        # We want to know whether or not a Maze should be saved as the same maze
        # or whether it is a new maze that goes to a new file
        # Only when we edit the name do we consider it a new maze
        self.maze_changed = False

        layout = QVBoxLayout()

        self.maze_drawer = maze_drawer
        self.maze = self.maze_drawer.maze

        self.maze_name_label = QLabel("")
        font = self.maze_name_label.font()
        font.setPointSize(25)
        self.maze_name_label.setFont(font)
        self.maze_name_label.setWordWrap(True)

        self.random_button = QPushButton("Randomize Maze")
        self.random_button.setEnabled(False)
        self.random_button.pressed.connect(self.randomize_maze)
        self.random_button.setFixedSize(150, 40)

        self.save_maze_button = QPushButton("Save Maze Changes")
        self.save_maze_button.setEnabled(False)
        self.save_maze_button.pressed.connect(self.save_maze)
        self.save_maze_button.setFixedSize(150, 40)

        self.load_selected_button = QPushButton("Load Selected Maze")
        self.load_selected_button.pressed.connect(self.load_selected_maze)
        self.load_selected_button.setFixedSize(150, 40)

        self.maze_list = QComboBox()
        self.maze_list.addItems(Maze.saved_mazes.keys())

        self.dimension_text = QLabel("Maze Size (x by x):")

        self.dimension_spin = QSpinBox()
        self.dimension_spin.setMinimum(5)
        self.dimension_spin.setMaximum(100)
        self.dimension_spin.setSingleStep(1)
        self.dimension_spin.valueChanged.connect(self.maze_dim_change)
        self.dimension_spin.setEnabled(False)

        self.new_maze_button = QPushButton("New Maze")
        self.new_maze_button.setFixedSize(150, 40)
        self.new_maze_button.pressed.connect(self.new_maze)

        self.difficulty_dial = QDial()
        self.difficulty_dial.setRange(0, 2)
        self.difficulty_dial.setSingleStep(1)
        self.difficulty_dial.valueChanged.connect(self.difficulty_change)
        self.difficulty_dial.setEnabled(False)
        self.difficulty_dial.setMaximumWidth(100)

        self.difficulty_text = QLabel("Difficulty:")

        self.maze_name_edit = QLineEdit()
        self.maze_name_edit.setPlaceholderText("Enter Maze Name")
        self.maze_name_edit.textEdited.connect(self.maze_name_change)
        self.maze_name_edit.setEnabled(False)

        self.help_button = QPushButton("Help")
        self.help_button.pressed.connect(self.show_help)
        self.help_button.setFixedSize(150, 40)

        self.place_start_button = QPushButton("Move Start")
        self.place_start_button.pressed.connect(self.place_start)
        self.place_start_button.setFixedSize(150, 40)
        self.place_start_button.setEnabled(False)
        self.place_end_button = QPushButton("Move End")
        self.place_end_button.pressed.connect(self.place_end)
        self.place_end_button.setFixedSize(150, 40)
        self.place_end_button.setEnabled(False)

        layout.addWidget(self.maze_name_label)
        layout.addWidget(self.maze_name_edit)
        layout.addWidget(self.maze_list)
        layout.addWidget(self.load_selected_button)
        layout.addWidget(self.new_maze_button)
        layout.addWidget(self.save_maze_button)
        layout.addWidget(self.random_button)
        layout.addWidget(self.dimension_text)
        layout.addWidget(self.dimension_spin)
        layout.addWidget(self.difficulty_text)
        layout.addWidget(self.difficulty_dial)
        layout.addWidget(self.place_start_button)
        layout.addWidget(self.place_end_button)
        layout.addWidget(self.help_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def place_start(self):
        self.maze_drawer.place_start = True

    def place_end(self):
        self.maze_drawer.place_end = True

    def update(self):
        self.maze_list.clear()
        self.maze_list.addItems(Maze.saved_mazes.keys())
        if not self.maze:
            return
        self.maze_name_label.setText(f"Editing {self.maze.name}")
        self.save_maze_button.setEnabled(True)
        self.dimension_spin.setEnabled(True)
        self.difficulty_dial.setEnabled(True)
        self.maze_name_edit.setEnabled(True)
        self.random_button.setEnabled(True)
        self.place_start_button.setEnabled(True)
        self.place_end_button.setEnabled(True)
        self.save_maze_button.show()

        self.save_maze_button.setText(
            "Save New Maze" if self.maze_changed else "Save Maze Changes"
        )
        self.difficulty_text.setText(
            f"Difficulty: {self.difficulty_options[self.difficulty_choice]}"
        )
        self.maze_name_edit.setText(self.maze.name)
        self.dimension_spin.setValue(self.maze.dim)
        if self.maze.name in Maze.saved_mazes:
            self.maze_list.setCurrentText(self.maze.name)
        self.maze_drawer.update()
        self.maze_drawer.repaint()
        self.maze_drawer.update()

    def save_maze(self):
        if not self.maze:
            return
        if not self.maze.route_astar(self.maze.start, self.maze.end, search_path=True):
            self.make_popup("That maze is not solvable!")
            return
        if self.maze_changed:
            if self.maze.name in Maze.saved_mazes:
                self.make_popup("That maze name already exists")
            else:
                self.maze.save_to_file()
                self.maze_changed = False
        else:
            self.maze.save_to_file(discard_old=True)
            self.maze_changed = False
        self.update()

    def load_selected_maze(self):
        if len(Maze.saved_mazes) == 0:
            self.make_popup("No saved mazes!")
        else:
            maze_selected = self.maze_list.currentText()
            self.maze = Maze.get_saved_maze(maze_selected)
            self.maze_changed = False
            self.maze_drawer.set_maze(self.maze)
            self.difficulty_text.setText(
                f"Difficulty: {self.difficulty_options[self.maze.difficulty]}"
            )
            self.difficulty_dial.setValue(self.maze.difficulty)
            self.maze_drawer.update()
            self.maze_drawer.repaint()
            self.update()

    def randomize_maze(self):
        self.maze.randomize()
        self.maze_drawer.update()

    def resize(self, width, height):
        self.setFixedSize(width, height)
        self.update()

    def difficulty_change(self, i):
        self.difficulty_choice = i
        self.maze.difficulty = i
        self.update()

    def name_change(self, name):
        self.maze.name = name
        self.update()

    def new_maze(self):
        self.maze = Maze("New Maze", 10, 0)
        self.maze_drawer.set_maze(self.maze)
        self.maze_changed = False
        self.update()

    def maze_dim_change(self, new_dim):
        self.maze.resize(new_dim)
        self.update()

    def maze_name_change(self, new_name):
        self.maze.name = new_name
        self.maze_changed = True
        self.maze_drawer.modified = False
        self.update()

    def show_help(self):
        help_message = (
            "Instructions: \n"
            "Edit the maze name by typing in the name box\n"
            "Choose a preexisting maze to edit in the drop-down and load it with the "
            "load button\n"
            "Create a new maze with the new button\n"
            "Save changes to the current maze with the save button\n"
            "Randomize the current maze with the random button, which uses the "
            "difficulty you set\n"
            "Configure the maze dimension with the number selector\n"
            "Change the difficulty by rotating the dial between the three "
            "difficulties\n"
            "Dragging/clicking the left mouse button places black borders on the maze\n"
            "Dragging/clicking the right mouse button places path tiles on the maze\n"
            "Move the start/end of the maze by clicking the appropriate button "
            "and then clicking on a valid start/ending tile\n"
        )
        self.make_popup(help_message, title="Help")

    def make_popup(self, message, title="Alert"):
        popup = QMessageBox(self)
        popup.setText(message)
        popup.setWindowTitle(title)
        ack = popup.exec()

        if ack:
            return
