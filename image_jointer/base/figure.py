from abc import ABC, abstractproperty, abstractmethod
from typing import Generator

from PIL import Image

from .vector import Vector

class Figure(ABC):
    @abstractproperty
    def width(self) -> int:
        ...

    @abstractproperty
    def height(self) -> int:
        ...

    @abstractmethod
    def paste(self, pos: Vector):
        ...

    @abstractmethod
    def draw(self, output: Image.Image, pos: Vector):
        ...
