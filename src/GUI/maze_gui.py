from collections import deque

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .Controls import header_bar
from .Screens import build_screen, home_screen, play_screen, share_screen


class MazeGUI(QMainWindow):
    """
    Base GUI object, renders all GUI screens inside of it
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snaking Mazes")
        self.setMinimumSize(1000, 560)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.screens = {
            "build": build_screen.BuildScreen(),
            "home": home_screen.HomeScreen(
                self.play_pressed, self.build_pressed, self.share_pressed
            ),
            "play": play_screen.PlayScreen(),
            "share": share_screen.ShareScreen(),
        }

        self.header = header_bar.HeaderBar(self.back_pressed, self.home_pressed, "")

        self.header.resize(self.width(), self.height() * 0.15)
        self.active_widget = self.screens["home"]
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.active_widget)

        self.screen_history = deque()
        self.screen_history.appendleft("home")
        self.active_widget.resize(self.width(), self.height() * 0.85)

    def set_active_screen(self, screen_name):
        if screen_name == "home":
            self.header.set_title("")
        if screen_name == "build":
            self.header.set_title("Build Maze")
        if screen_name == "play":
            self.header.set_title("Play Maze")
        if screen_name == "share":
            self.header.set_title("Share Mazes")

        self.layout.addWidget(self.header)
        self.layout.removeWidget(self.active_widget)
        self.active_widget.setParent(None)
        self.active_widget = self.screens[screen_name]
        self.layout.addWidget(self.active_widget)

        self.screen_history.appendleft(screen_name)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.header.resize(self.width(), self.height() * 0.15)
        self.active_widget.resize(self.width(), self.height() * 0.85)

    def home_pressed(self):
        self.set_active_screen("home")

    def back_pressed(self):
        self.screen_history.popleft()
        self.set_active_screen(self.screen_history[-1])

    def build_pressed(self):
        self.set_active_screen("build")

    def play_pressed(self):
        self.set_active_screen("play")

    def share_pressed(self):
        self.set_active_screen("share")
