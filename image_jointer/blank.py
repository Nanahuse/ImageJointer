from dataclasses import dataclass

from .interfaces import iSize


@dataclass(frozen=True)
class Blank(iSize):
    _width: int
    _height: int

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height
