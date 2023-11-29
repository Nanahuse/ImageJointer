# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from __future__ import annotations
from typing import overload

from PIL import Image

from .base.blank import Blank
from .base.enums import JointAlign
from .base.interfaces import _iSize
from .base.part import _Part
from .base.vector import Vector


class ImageJointer(_iSize):
    def __init__(self, source: Image.Image | Blank | ImageJointer | None = None) -> None:
        """_summary_

        Args:
            source (Image.Image | Blank | ImageJointer | None): 画像をつなげていく元となるもの。default to None

        Raises:
            ValueError: _description_
        """
        match source:
            case Image.Image() | Blank():
                self.__parts: tuple[_Part] = (_Part(source),)
                self.__width = source.width
                self.__height = source.height
            case ImageJointer():
                self.__parts = source.__parts
                self.__width = source.width
                self.__height = source.height
            case None:
                self.__parts: tuple[_Part] = tuple()
                self.__width = 0
                self.__height = 0
            case _:
                raise ValueError()

    @classmethod
    def __make_from_tuple(cls, parts: tuple[_Part]) -> None:
        instance = ImageJointer()
        instance.__parts = parts
        instance.__width = max(part.position.x + part.width for part in instance.__parts)
        instance.__height = max(part.position.y + part.height for part in instance.__parts)
        return instance

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @overload
    def joint(self, image: Image.Image | _iSize, align: JointAlign) -> ImageJointer:
        """
        自身の右または下に別の画像を接続した新しい画像を作成する。
        実際にはto_image実行時まで画像生成は遅延される。

        Args:
            image (Image.Image | _iSize): 接続する画像

            align (JointAlign): 整列方法

        Returns:
            ImageJointer: メソッドチェーン可能。副作用はない。
        """
        ...

    @overload
    def joint(
        self,
        images: tuple[Image.Image | _iSize] | list[Image.Image | _iSize],
        align: JointAlign,
    ) -> ImageJointer:
        """
        自身の右または下に別の画像を連続して接続した新しい画像を作成する。
        実際にはto_image実行時まで画像生成は遅延される。

        Args:
            images (tuple | list): 接続する画像

            align (JointAlign): 整列方法

        Returns:
            ImageJointer: メソッドチェーン可能。副作用はない。
        """
        ...

    def joint(self, image: Image.Image | _iSize | tuple | list, align: JointAlign) -> ImageJointer:
        def chain_source_move(move_to: Vector | None, paste_position: Vector):
            for tmp in self.__parts:
                if move_to is None:
                    yield tmp
                else:
                    yield tmp.move(move_to)
            match image:
                case Image.Image() | Blank():
                    yield _Part(image, paste_position)
                case ImageJointer():
                    for tmp_image in image.__parts:
                        yield tmp_image.move(paste_position)
                case _:
                    ValueError("image should be PIL.Image.Image or Blank or ImageJointer")

        if isinstance(image, (tuple, list)):
            jointed = ImageJointer()
            for element in image:
                jointed.joint(element, align)
            return jointed

        if not isinstance(image, (Image.Image, _iSize)):
            raise ValueError("image is invalid type")

        match align:
            case JointAlign.SIDE_TOP:
                position = Vector(self.width, 0)
                return ImageJointer.__make_from_tuple(tuple(chain_source_move(None, position)))
            case JointAlign.SIDE_CENTER | JointAlign.SIDE_BOTTOM:
                if align is JointAlign.SIDE_CENTER:
                    height = (self.height - image.height) // 2
                else:
                    height = self.height - image.height
                if height >= 0:
                    position = Vector(self.width, height)
                    return ImageJointer.__make_from_tuple(tuple(chain_source_move(None, position)))
                else:
                    move_to = Vector(0, -height)
                    position = Vector(self.width, 0)
                    return ImageJointer.__make_from_tuple(tuple(chain_source_move(move_to, position)))

            case JointAlign.UNDER_LEFT:
                position = Vector(0, self.height)
                return ImageJointer.__make_from_tuple(tuple(chain_source_move(None, position)))
            case JointAlign.UNDER_CENTER | JointAlign.UNDER_RIGHT:
                if align is JointAlign.UNDER_CENTER:
                    width = (self.width - image.width) // 2
                else:
                    width = self.width - image.width
                if width >= 0:
                    position = Vector(width, self.height)
                    return ImageJointer.__make_from_tuple(tuple(chain_source_move(None, position)))
                else:
                    move_to = Vector(-width, 0)
                    position = Vector(0, self.height)
                    return ImageJointer.__make_from_tuple(tuple(chain_source_move(move_to, position)))
            case _:
                ValueError("align is invalid type")

    def to_image(self):
        """
        画像を生成する。

        Returns:
            Image.Image: 生成された画像
        """
        output = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        for part in self.__parts:
            part.paste_to(output)
        return output
