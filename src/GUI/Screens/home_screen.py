from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout

from .screen import Screen


class HomeScreen(Screen):
    """
    Main home screen of application
    Extends Screen
    """

    def __init__(
        self, play_button_callback, build_button_callback, share_button_callback
    ):
        """
        Initializes a HomeScreen
        @param play_button_calback: Function to call when play is pressed
        @param build_button_callback: Function to call when build is pressed
        @param share_button_callback: Function to call when share is pressed
        """
        super().__init__()

        title_widget = QLabel("Snaking Mazes")
        title_font = title_widget.font()
        title_font.setPointSize(50)
        title_widget.setFont(title_font)
        title_widget.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        author_widget = QLabel("By Sam Haggans")
        author_font = author_widget.font()
        author_font.setPointSize(30)
        author_widget.setFont(author_font)
        author_widget.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        play_button = QPushButton("Play Mazes")
        play_button.pressed.connect(play_button_callback)
        play_button.setFixedHeight(40)

        build_button = QPushButton("Build Mazes")
        build_button.pressed.connect(build_button_callback)
        build_button.setFixedHeight(40)
        share_button = QPushButton("Share Mazes")
        share_button.pressed.connect(share_button_callback)
        share_button.setFixedHeight(40)

        layout = QVBoxLayout()
        layout.addWidget(title_widget)
        layout.addWidget(author_widget)
        layout.addWidget(play_button)
        layout.addWidget(build_button)
        layout.addWidget(share_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.addStretch()
        self.setLayout(layout)
