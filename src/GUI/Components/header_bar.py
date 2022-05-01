from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class HeaderBar(QWidget):
    """
    Represents the header bar of the application
    Provides back and home buttons and provides a title for each screen
    Extends QWidget
    """

    def __init__(self, back_pressed_callback, home_pressed_callback, title):
        """
        Initializes header bar
        @param back_pressed_callback: Callback function for when back button is pressed
        @param home_pressed_callback: Callback function for when home button is pressed
        @param title: Title to display at the top of the bar
        """
        super().__init__()

        layout = QHBoxLayout()

        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(100, 30)
        self.back_button.pressed.connect(back_pressed_callback)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        font = self.title_label.font()
        font.setPointSize(30)
        self.title_label.setFont(font)

        self.home_button = QPushButton("Home")
        self.home_button.setFixedSize(100, 30)
        self.home_button.pressed.connect(home_pressed_callback)

        layout.addWidget(self.back_button)
        layout.addWidget(self.title_label)
        layout.addWidget(self.home_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def set_title(self, title):
        """
        Sets the title of the header bar
        @param title: Title to display
        """
        self.title_label.setText(title)

    def resize(self, width, height):
        """
        Resizes header bar
        @param width: New width in pixels
        @param height: New height in pixels
        """
        self.setFixedSize(width, height)
