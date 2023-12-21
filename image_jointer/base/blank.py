from dataclasses import dataclass

from PIL import Image

from .part import _Part
from .figure import Figure
from .vector import Vector


@dataclass(frozen=True)
class Blank(Figure):
    _width: int
    _height: int

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def paste(self, pos: Vector):
        yield _Part(self, pos)

    def draw(self, output: Image.Image, pos: Vector):
        pass
