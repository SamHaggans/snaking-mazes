from PyQt6.QtWidgets import QLabel, QMainWindow

from .Screens import build_screen, home_screen, play_screen, setup_screen, share_screen


class MazeGUI(QMainWindow):
    """
    Base GUI object, renders all GUI screens inside of it
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snaking Mazes")

        title_widget = QLabel("Snaking Mazes")

        self.setCentralWidget(title_widget)

        self.screens = {
            "build": build_screen.BuildScreen(),
            "home": home_screen.HomeScreen(),
            "play": play_screen.PlayScreen(),
            "setup": setup_screen.SetupScreen(),
            "share": share_screen.ShareScreen(),
        }

        self.active_screen = self.screens["home"]
