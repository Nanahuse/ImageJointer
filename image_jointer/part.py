from dataclasses import dataclass

from PIL import Image

from .blank import Blank
from .interfaces import iSize
from .vector import Vector


@dataclass(frozen=True)
class Part(iSize):
    source: Image.Image | Blank
    position: Vector = Vector()

    @property
    def width(self) -> int:
        return self.source.width

    @property
    def height(self) -> int:
        return self.source.height

    def move(self, vector: Vector):
        return Part(self.source, self.position + vector)

    def paste_to(self, output: Image.Image):
        match self.source:
            case Image.Image():
                output.paste(self.source, (self.position.x, self.position.y))
            case Blank():
                pass
            case _:
                raise RuntimeError()
