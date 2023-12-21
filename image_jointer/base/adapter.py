from dataclasses import dataclass
from typing import Generator

from PIL import Image

from .figure import Figure
from .part import _Part
from .vector import Vector

@dataclass(frozen=True)
class ImageAdapter(Figure):
    image: Image.Image

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    def paste(self, pos: Vector) -> Generator[_Part, None, None]:
        yield _Part(self, pos)

    def draw(self, output: Image.Image, pos: Vector):
        output.paste(self.image, (pos.x, pos.y))
