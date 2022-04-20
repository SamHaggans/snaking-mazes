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

        self.elapsed_time = 0.0
        self.play_timer_label = QLabel("0.0")
        self.play_timer_label.setFont(font)

        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.update_time)

        self.play_timer_enabled = False
        self.play_button = QPushButton("Start Play Timer")
        self.play_button.pressed.connect(self.toggle_play_timer)
        self.play_button.setFixedSize(150, 40)
        self.play_button.setEnabled(False)

        self.reset_play_button = QPushButton("Reset Play Timer")
        self.reset_play_button.pressed.connect(self.clear_timer)
        self.reset_play_button.setFixedSize(150, 40)

        self.help_button = QPushButton("Help")
        self.help_button.pressed.connect(self.show_help)
        self.help_button.setFixedSize(150, 40)

        self.maze_drawer.set_draw_end_func(self.stop_play_timer)

        self.maze_list = QComboBox()
        self.maze_list.addItems(Maze.saved_mazes.keys())

        layout.addWidget(self.maze_name_label)
        layout.addWidget(self.maze_list)
        layout.addWidget(self.load_selected_button)
        layout.addWidget(self.clear_maze_button)
        layout.addWidget(self.animate_solve_button)
        layout.addWidget(self.play_timer_label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.reset_play_button)
        layout.addWidget(self.help_button)
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
        self.play_button.setEnabled(True)
        self.maze_name_label.setText(self.maze.name)
        if self.maze.name in Maze.saved_mazes:
            self.maze_list.setCurrentText(self.maze.name)
        self.maze_name_label.setFixedWidth(self.width())
        self.maze_drawer.repaint()
        self.maze_drawer.update()

    def clear_timer(self):
        if self.play_timer_enabled:
            self.toggle_play_timer()
        self.elapsed_time = 0.0
        self.play_timer_label.setText(str(self.elapsed_time))

    def stop_play_timer(self):
        if self.play_timer_enabled:
            self.toggle_play_timer()

    def toggle_play_timer(self):
        if not self.play_timer_enabled:
            self.play_button.setText("Stop Timer")
            self.elapsed_time = 0.0
            self.play_timer_label.setText(str(self.elapsed_time))
            self.play_timer.start(100)
        else:
            self.play_button.setText("Start Timer")
            self.play_timer.stop()
        self.play_timer_enabled = not self.play_timer_enabled

    def update_time(self):
        self.elapsed_time += 0.1
        self.elapsed_time = round(self.elapsed_time, 1)
        self.play_timer_label.setText(str(self.elapsed_time))

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

    def show_help(self):
        help_message = (
            "Instructions: \n"
            "Choose the maze you want to play from the drop-down menu and click the "
            "load button\n"
            "Use the left mouse button and click or drag to mark the maze path \n"
            "You can remove parts of the path by clicking or dragging with the right "
            "mouse button\n"
            "You can watch an algorithm solve the maze by pressing the 'Watch Solver' "
            "button\n"
            "You can also set a timer for yourself (or the algorithm) to time the "
            "solve \n"
        )
        self.make_popup(help_message, title="Help")

    def make_popup(self, message, title="Alert"):
        popup = QMessageBox(self)
        popup.setText(message)
        popup.setWindowTitle(title)
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
