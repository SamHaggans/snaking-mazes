from PyQt6.QtCore import Qt, QTimer
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
        self.animation_state = {
            "nodes": None,
            "node_from": None,
            "g_score": None,
            "f_score": None,
        }

        layout = QVBoxLayout()
        self.solving = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_animation_tick)

        self.maze_name_label = QLabel("")
        font = self.maze_name_label.font()
        font.setPointSize(25)
        self.maze_name_label.setFont(font)
        self.maze_name_label.setWordWrap(True)
        self.maze_name_label.setFixedWidth(self.width())

        self.maze_drawer = maze_drawer
        self.maze_drawer.mode = 1
        self.maze = self.maze_drawer.maze

        self.load_selected_button = QPushButton("Load Selected Maze")
        self.load_selected_button.pressed.connect(self.load_selected_maze)
        self.load_selected_button.setFixedSize(150, 40)

        self.clear_maze_button = QPushButton("Clear Path")
        self.clear_maze_button.pressed.connect(self.clear_maze)
        self.clear_maze_button.setFixedSize(150, 40)
        self.clear_maze_button.setEnabled(False)

        self.animate_solve_button = QPushButton("Watch Solver")
        self.animate_solve_button.pressed.connect(self.toggle_solver)
        self.animate_solve_button.setFixedSize(150, 40)
        self.animate_solve_button.setEnabled(False)

        self.maze_list = QComboBox()
        self.maze_list.addItems(Maze.saved_mazes.keys())

        layout.addWidget(self.maze_name_label)
        layout.addWidget(self.maze_list)
        layout.addWidget(self.load_selected_button)
        layout.addWidget(self.clear_maze_button)
        layout.addWidget(self.animate_solve_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def update(self):
        Maze.load_saved_mazes()
        self.maze_list.clear()
        self.maze_list.addItems(Maze.saved_mazes.keys())
        if not self.maze:
            return
        self.clear_maze_button.setEnabled(True)
        self.animate_solve_button.setEnabled(True)
        self.maze_name_label.setText(self.maze.name)
        if self.maze.name in Maze.saved_mazes:
            self.maze_list.setCurrentText(self.maze.name)
        self.maze_name_label.setFixedWidth(self.width())
        self.maze_drawer.repaint()
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
        self.solving = False
        self.load_selected_maze()

    def make_popup(self, message):
        popup = QMessageBox(self)
        popup.setWindowTitle("Alert")
        popup.setText(message)
        ack = popup.exec()

        if ack:
            return

    def toggle_solver(self):
        if not self.solving:
            self.clear_maze()
            self.animate_solve_button.setText("Stop Solver")
            self.timer.start(int(50 * (10 / self.maze.dim)))
            self.animation_state = {
                "nodes": None,
                "node_from": None,
                "g_score": None,
                "f_score": None,
            }
        else:
            self.timer.stop()
            self.animate_solve_button.setText("Start Solver")
        self.solving = not self.solving

    def run_animation_tick(self):
        result = self.maze.route_astar(
            self.maze.start,
            self.maze.end,
            animate=True,
            search_path=True,
            nodes=self.animation_state["nodes"],
            node_from=self.animation_state["node_from"],
            g_score=self.animation_state["g_score"],
            f_score=self.animation_state["f_score"],
        )
        if type(result) == tuple:
            self.animation_state = {
                "nodes": result[0],
                "node_from": result[1],
                "g_score": result[2],
                "f_score": result[3],
            }
        else:
            # disable solver
            self.toggle_solver()
        self.update()
