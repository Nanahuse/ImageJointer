from __future__ import annotations

from abc import ABC, abstractproperty, abstractmethod
from typing import TYPE_CHECKING, Generator

from PIL import Image

from .vector import Vector

if TYPE_CHECKING:
    from .part import _Part


class Figure(ABC):
    @abstractproperty
    def width(self) -> int:
        ...

    @abstractproperty
    def height(self) -> int:
        ...

    @abstractmethod
    def _paste(self, pos: Vector) -> Generator[_Part, None, None]:
        ...

    @abstractmethod
    def _draw(self, output: Image.Image, pos: Vector):
        ...
