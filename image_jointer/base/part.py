from dataclasses import dataclass

from PIL import Image

from .figure import Figure
from .vector import Vector


@dataclass(frozen=True)
class _Part:
    source: Figure
    position: Vector = Vector()

    @property
    def width(self) -> int:
        return self.source.width

    @property
    def height(self) -> int:
        return self.source.height

    def shift(self, shift_to: Vector):
        return _Part(self.source, self.position + shift_to)

    def draw(self, output: Image.Image):
        self.source._draw(output, self.position)
