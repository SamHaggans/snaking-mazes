from PyQt6.QtCore import Qt

from src.GUI.maze_gui import MazeGUI

"""
The GUI is difficult to test with automated tests
and is also relatively easy to verify manually
I define a few basic tests here to check general GUI functionality
"""


def test_home(qtbot):
    """
    Tests that we start at the home screen
    """
    test_gui = MazeGUI(hidden=True)
    assert test_gui.active_widget == test_gui.screens["home"]


def test_home_and_back(qtbot):
    """
    Tests that we can go to the play menu, click home, then click back
    and we end up back at play
    """
    test_gui = MazeGUI(hidden=True)
    qtbot.addWidget(test_gui)
    qtbot.mouseClick(test_gui.active_widget.play_button, Qt.MouseButton.LeftButton)
    # We should get to the play screen
    assert test_gui.active_widget == test_gui.screens["play"]
    qtbot.mouseClick(test_gui.header.home_button, Qt.MouseButton.LeftButton)
    # We should get to the home screen
    assert test_gui.active_widget == test_gui.screens["home"]
    qtbot.mouseClick(test_gui.header.back_button, Qt.MouseButton.LeftButton)
    # We should now be back at the play screen
    assert test_gui.active_widget == test_gui.screens["play"]
    qtbot.mouseClick(test_gui.header.back_button, Qt.MouseButton.LeftButton)
    # And finally back at the home screen
    assert test_gui.active_widget == test_gui.screens["home"]
