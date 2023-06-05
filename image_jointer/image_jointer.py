# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from __future__ import annotations
from abc import ABC, abstractproperty
from enum import Enum, auto
from dataclasses import dataclass
from PIL import Image


class Aline(Enum):
    # 元画像の右側に連結する。
    SideTop = auto()  # 上端ぞろえ
    SideCenter = auto()  # 中心ぞろえ
    SideBottom = auto()  # 下端ぞろえ
    # 元画像の下側に連結する。
    DownLeft = auto()  # 左端ぞろえ
    DownCenter = auto()  # 中心ぞろえ
    DownRight = auto()  # 右端ぞろえ


class iSize(ABC):
    @abstractproperty
    def width(self) -> int:
        pass

    @abstractproperty
    def height(self) -> int:
        pass


@dataclass(frozen=True)
class Position:
    x: int = 0
    y: int = 0

    def move(self, x: int, y: int):
        return Position(self.x + x, self.y + y)


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


class ImageJointer(iSize):
    @dataclass(frozen=True)
    class _Part(iSize):
        source: Image.Image | Blank
        position: Position = Position()

        @property
        def width(self) -> int:
            return self.source.width

        @property
        def height(self) -> int:
            return self.source.height

        def move(self, x: int, y: int):
            return ImageJointer._Part(self.source, self.position.move(x, y))

        def paste_to(self, output: Image.Image):
            if isinstance(self.source, Image.Image):
                output.paste(self.source, (self.position.x, self.position.y))

    def __init__(self, source: Image.Image | Blank | None = None) -> None:
        """_summary_

        Args:
            source (Image.Image | Blank | None): 画像をつなげていく元となるもの。画像なしも可

        Raises:
            ValueError: _description_
        """
        match source:
            case Image.Image() | Blank():
                self._parts: tuple[ImageJointer._Part] = (ImageJointer._Part(source),)
                self._width = source.width
                self._height = source.height
            case None:
                self._parts: tuple[ImageJointer._Part] = tuple()
                self._width = 0
                self._height = 0
            case tuple():
                self._parts: tuple[ImageJointer._Part] = source
                self._width = max(part.position.x + part.width for part in self._parts)
                self._height = max(part.position.y + part.height for part in self._parts)
            case _:
                raise ValueError()

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def move(self, x: int, y: int):
        return ImageJointer(tuple(tmp.move(x, y) for tmp in self._parts))

    def joint(self, image: Image.Image | Blank | ImageJointer, aline: Aline) -> ImageJointer:
        """
        to_image実行時まで画像は生成されない。

        Args:
            image (Image.Image | iSize): 接続する画像
            aline (Aline): 整列方法

        Returns:
            ImageJointer: メソッドチェーン可能。副作用はない。
        """

        def chain_source_move(move_to: Position | None, paste_position: Position):
            for tmp in self._parts:
                if move_to is None:
                    yield tmp
                else:
                    yield tmp.move(move_to.x, move_to.y)
            match image:
                case Image.Image() | Blank():
                    yield ImageJointer._Part(image, paste_position)
                case ImageJointer():
                    for tmp_image in image._parts:
                        yield tmp_image.move(paste_position.x, paste_position.y)
                case _:
                    ValueError("image should be PIL.Image.Image or Blank or ImageJointer")

        match aline:
            case Aline.SideTop:
                position = Position(self.width, 0)
                return ImageJointer(tuple(chain_source_move(None, position)))
            case Aline.SideCenter | Aline.SideBottom:
                if aline is Aline.SideCenter:
                    height = (self.height - image.height) // 2
                else:
                    height = self.height - image.height
                if height >= 0:
                    position = Position(self.width, height)
                    return ImageJointer(tuple(chain_source_move(None, position)))
                else:
                    move_to = Position(0, -height)
                    position = Position(self.width, 0)
                    return ImageJointer(tuple(chain_source_move(move_to, position)))

            case Aline.DownLeft:
                position = Position(0, self.height)
                return ImageJointer(tuple(chain_source_move(None, position)))
            case Aline.DownCenter | Aline.DownRight:
                if aline is Aline.DownCenter:
                    width = (self.width - image.width) // 2
                else:
                    width = self.width - image.width
                if width >= 0:
                    position = Position(width, self.height)
                    return ImageJointer(tuple(chain_source_move(None, position)))
                else:
                    move_to = Position(-width, 0)
                    position = Position(0, self.height)
                    return ImageJointer(tuple(chain_source_move(move_to, position)))
            case _:
                ValueError()

    def to_image(self):
        output = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        for part in self._parts:
            part.paste_to(output)
        return output
