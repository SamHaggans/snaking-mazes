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
    Represents editing controls for a maze
    Extends QWidget
    """

    def __init__(self, maze_drawer):
        """
        Initializes an EditControl widget
        @param maze_drawer: MazeDrawer widget linked to the edit controls
        """
        super().__init__()
        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_choice = 0

        # We want to know whether or not a Maze should be saved as the same maze
        # or whether it is a new maze that goes to a new file
        # Only when we edit the name do we consider it a new maze
        self.maze_changed = False

        layout = QVBoxLayout()

        # Set params for maze and maze_drawer
        self.maze_drawer = maze_drawer
        self.maze = None

        # Label for maze name
        self.maze_name_label = QLabel("")
        font = self.maze_name_label.font()
        font.setPointSize(25)
        self.maze_name_label.setFont(font)
        self.maze_name_label.setWordWrap(True)

        # Randomize maze button
        self.random_button = QPushButton("Randomize Maze")
        self.random_button.setEnabled(False)
        self.random_button.pressed.connect(self.randomize_maze)
        self.random_button.setFixedSize(150, 40)

        # Save maze button
        self.save_maze_button = QPushButton("Save Maze Changes")
        self.save_maze_button.setEnabled(False)
        self.save_maze_button.pressed.connect(self.save_maze)
        self.save_maze_button.setFixedSize(150, 40)

        # Load maze button
        self.load_selected_button = QPushButton("Load Selected Maze")
        self.load_selected_button.pressed.connect(self.load_selected_maze)
        self.load_selected_button.setFixedSize(150, 40)

        # Saved maze dropdown list
        self.maze_list = QComboBox()
        self.maze_list.addItems(Maze.saved_mazes.keys())

        # Label for maze size
        self.dimension_text = QLabel("Maze Size (x by x):")

        # Size number spin edit
        self.dimension_spin = QSpinBox()
        # Bounds are 5-100 just because of reasonability of displaying mazes
        # theoretically > 100 would be fine but it gets
        # too hard to see/click at that scale
        self.dimension_spin.setMinimum(5)
        self.dimension_spin.setMaximum(100)
        self.dimension_spin.setSingleStep(1)
        self.dimension_spin.valueChanged.connect(self.maze_dim_change)
        self.dimension_spin.setEnabled(False)

        # New maze button
        self.new_maze_button = QPushButton("New Maze")
        self.new_maze_button.setFixedSize(150, 40)
        self.new_maze_button.pressed.connect(self.new_maze)

        # Difficulty dial
        self.difficulty_dial = QDial()
        self.difficulty_dial.setRange(0, 2)
        self.difficulty_dial.setSingleStep(1)
        self.difficulty_dial.valueChanged.connect(self.difficulty_change)
        self.difficulty_dial.setEnabled(False)
        self.difficulty_dial.setMaximumWidth(100)

        # Difficulty text label
        self.difficulty_text = QLabel("Difficulty:")

        # Maze name edit
        self.maze_name_edit = QLineEdit()
        self.maze_name_edit.setPlaceholderText("Enter Maze Name")
        self.maze_name_edit.textEdited.connect(self.maze_name_change)
        self.maze_name_edit.setEnabled(False)

        # Button to open help pop-up
        self.help_button = QPushButton("Help")
        self.help_button.pressed.connect(self.show_help)
        self.help_button.setFixedSize(150, 40)

        # Buttons to move start and end
        self.place_start_button = QPushButton("Move Start")
        self.place_start_button.pressed.connect(self.place_start)
        self.place_start_button.setFixedSize(150, 40)
        self.place_start_button.setEnabled(False)
        self.place_end_button = QPushButton("Move End")
        self.place_end_button.pressed.connect(self.place_end)
        self.place_end_button.setFixedSize(150, 40)
        self.place_end_button.setEnabled(False)

        # Add all of the widgets to the layout top to bottom
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
        """
        Tells the maze drawer to interpret next mouse event as an attempt
        to move start of maze
        """
        self.maze_drawer.place_start = True

    def place_end(self):
        """
        Tells the maze drawer to interpret next mouse event as an attempt
        to move end of maze
        """
        self.maze_drawer.place_end = True

    def update(self):
        """
        Updates the widget, called by PyQT
        """
        # Add mazes to the list to account for any changes/new saved mazes
        self.maze_list.clear()
        self.maze_list.addItems(Maze.saved_mazes.keys())
        # The rest of the controls all need a maze to exist, so exit if we
        # don't have one yet
        if not self.maze:
            return
        # Enable all the buttons and text once we have a maze
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
        # We set the currently selected maze in the dropdown to the maze
        # we have if it is saved because it looks nicer
        if self.maze.name in Maze.saved_mazes:
            self.maze_list.setCurrentText(self.maze.name)
        # Update the maze drawer to save maze changes
        self.maze_drawer.update()

    def save_maze(self):
        """
        Called when the maze save button is pressed
        """
        if not self.maze:
            return
        # Make sure that the given maze is solvable
        if not self.maze.route_astar(self.maze.start, self.maze.end, search_path=True):
            self.make_popup("That maze is not solvable!")
            return
        # Here we check if a maze is a "new" maze or an edited maze
        # based on the criteria described in __init__ above
        # If it is a "new" maze, we don't allow it to be saved with the
        # same name as another maze
        if self.maze_changed:
            if self.maze.name in Maze.saved_mazes:
                self.make_popup("That maze name already exists")
            else:
                self.maze.save_to_file()
                self.maze_changed = False
        # else case is if it is the same maze, just edited
        # in which case we want to overwrite the old one
        else:
            self.maze.save_to_file(discard_old=True)
            self.maze_changed = False
        self.update()

    def load_selected_maze(self):
        """
        Loads the selected maze from the drop down menu
        """
        # Make sure there are mazes we can load
        if len(Maze.saved_mazes) == 0:
            self.make_popup("No saved mazes!")
        else:
            # Get the current saved maze
            maze_selected = self.maze_list.currentText()
            self.maze = Maze.get_saved_maze(maze_selected)
            self.maze_changed = False
            self.maze_drawer.set_maze(self.maze)
            self.update()

    def randomize_maze(self):
        """
        Triggers when the randomize button is pressed to randomize the maze
        """
        self.maze.randomize()
        self.update()

    def resize(self, width, height):
        """
        Resizes the window on a PyQT resize event
        @param width: New width
        @param height: New height
        """
        self.setFixedSize(width, height)
        self.update()

    def difficulty_change(self, i):
        """
        Triggers when the difficulty choice is changed
        @param i: Index of new wheel position
        """
        self.difficulty_choice = i
        self.maze.difficulty = i
        self.update()

    def new_maze(self):
        """
        Triggers when the new maze button is pressed
        """
        self.maze = Maze("New Maze", 10, 0)
        self.maze_drawer.set_maze(self.maze)
        self.maze_changed = False
        self.update()

    def maze_dim_change(self, new_dim):
        """
        Triggers when the dimension of the maze is changed
        @param new_dim: New dimension size
        """
        self.maze.resize(new_dim)
        self.update()

    def maze_name_change(self, new_name):
        """
        Triggered when the name of the maze is changed
        @param new_name: String of new maze name
        """
        self.maze.name = new_name
        self.maze_changed = True
        self.maze_drawer.modified = False
        self.update()

    def show_help(self):
        """
        Displays a pop-up with the help message
        """
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
        """
        Creates a pop-up window with a given text
        @param message: Main message to display in the pop-up
        @param title: Title to give to pop-up window, default 'Alert'
        """
        popup = QMessageBox(self)
        popup.setText(message)
        popup.setWindowTitle(title)
        ack = popup.exec()

        if ack:
            return
