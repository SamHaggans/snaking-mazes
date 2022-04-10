from abc import ABC, abstractmethod


class Screen(ABC):
    """
    Base class for GUI screens
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
