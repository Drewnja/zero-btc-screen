from abc import ABC, abstractmethod

class Page(ABC):
    @abstractmethod
    def render(self, draw, width, height):
        pass

    @abstractmethod
    def update_data(self, data):
        pass

