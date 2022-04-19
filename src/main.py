from PyQt6.QtWidgets import QApplication

from src.GUI.maze_gui import MazeGUI

if __name__ == "__main__":
    app = QApplication([])
    window = MazeGUI()
    window.show()
    app.exec()
