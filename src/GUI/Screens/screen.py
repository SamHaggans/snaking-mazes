from PyQt6.QtWidgets import QWidget


class Screen(QWidget):
    """
    Base class for GUI screens
    Currently mostly unused, but still useful as a general base class
    """

    def __init__(self):
        """
        Initializes a screen
        """
        super().__init__()

    def resize(self, width, height):
        """
        Triggered when the screen is resized
        Generally overridden by subclasses
        @param width: New width in pixels
        @param height: New height in pixels
        """
        self.setFixedSize(width, height)
