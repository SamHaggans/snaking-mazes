from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget


class MazeDrawer(QWidget):
    def __init__(self):
        super().__init__()
        self.painter = QPainter()
        self.painter.begin()
