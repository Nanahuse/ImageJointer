# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from __future__ import annotations
from typing import assert_never

from PIL import Image

from .base.enums import JointAlignment
from .base.figure import Figure
from .base.adapter import ImageAdapter
from .base.part import _Part
from .base.vector import Vector


class ImageJointer(Figure):
    __parts: tuple[_Part, ...]

    def __init__(self, source: Image.Image | Figure | None = None) -> None:
        """
        Building up image by jointing images.
        Building image will be postponed until execute to_image.
        Method chainable.

        Args:
            source (Image.Image | Figure | None): source of building up. default to None

        Raises:
            ValueError: raise if source is invalid type
        """
        match source:
            case Image.Image():
                source = ImageAdapter(source)

        match source:
            case ImageJointer():
                self.__parts = source.__parts
                self.__width = source.width
                self.__height = source.height
            case None:
                self.__parts = tuple()
                self.__width = 0
                self.__height = 0
            case _:
                self.__parts = (_Part(source),)
                self.__width = source.width
                self.__height = source.height

    @classmethod
    def __make_from_tuple(cls, parts: tuple[_Part, ...]) -> ImageJointer:
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

    def _paste(self, paste_to: Vector):
        for part in self.__parts:
            yield part.shift(paste_to)

    def _draw(self, output: Image.Image, pos: Vector):
        for part in self.__parts:
            part.draw(output)

    def __calc_shift(self, diff: Vector) -> Vector:
        """
        Calculate shift position for primary part from absolute paste position.
        To image centering, if secondary part is larger than primary part,
        we need to move primary part from original position to acquire gap.
        In such situation, this function returns desired position shift length.
        """
        return Vector(-min(0, diff.x), -min(0, diff.y))

    def __calc_paste(self, diff: Vector) -> Vector:
        """
        Calculate paste position for secondary part from absolute paste position.
        To image centering, if primary part is larger than secondary part,
        we need to take gap from original position.
        In such situation, this function returns desired paste position.
        """
        return Vector(+max(0, diff.x), +max(0, diff.y))

    def __calc_absolute_paste_pos(self, align: JointAlignment, image: Figure) -> Vector:
        """
        Calculate absolute paste position from desired alignment.
        Despite of real image area,
        We assume infinite =(-inf, +inf) area for images in this function.
        We call this imaginary position as absolute paste position.
        But this assume is not real condition
        so we need to calculate real relative moves
        from this positions for primary/secondary parts.
        Such conversion is implemented as calc_shift() and calc_paste().
        """
        match align:
            case JointAlignment.RIGHT_TOP:
                return Vector(self.width, 0)
            case JointAlignment.RIGHT_CENTER:
                return Vector(self.width, (self.height - image.height) // 2)
            case JointAlignment.RIGHT_BOTTOM:
                return Vector(self.width, self.height - image.height)
            case JointAlignment.DOWN_LEFT:
                return Vector(0, self.height)
            case JointAlignment.DOWN_CENTER:
                return Vector((self.width - image.width) // 2, self.height)
            case JointAlignment.DOWN_RIGHT:
                return Vector(self.width - image.width, self.height)
            case _ as unreachable:
                assert_never(unreachable)

    def __run_joint(self, image: Figure, shift_to: Vector, paste_to: Vector):
        for tmp in self.__parts:
            yield tmp.paste(shift_to)
        yield from image._paste(paste_to)

    def joint_single(self, align: JointAlignment, image: Image.Image | Figure) -> ImageJointer:
        """
        Joint new image to right side or bottom.
        There are no side effect.

        Args:
            align (JointAlignment): how to align image

            image (Image.Image | Figure): image to joint

        Returns:
            ImageJointer: New instance of jointed image. Method chainable.
        """
        if not isinstance(image, (Image.Image, Figure)):
            raise ValueError("Image is invalid type")
        if not isinstance(align, JointAlignment):
            raise ValueError("align is invalid type")

        match image:
            case Image.Image():
                image = ImageAdapter(image)

        match align:
            case JointAlignment.UP_LEFT:
                return ImageJointer().joint(JointAlignment.DOWN_LEFT, image, self)
            case JointAlignment.UP_CENTER:
                return ImageJointer().joint(JointAlignment.DOWN_CENTER, image, self)
            case JointAlignment.UP_RIGHT:
                return ImageJointer().joint(JointAlignment.DOWN_RIGHT, image, self)
            case JointAlignment.LEFT_TOP:
                return ImageJointer().joint(JointAlignment.RIGHT_TOP, image, self)
            case JointAlignment.LEFT_CENTER:
                return ImageJointer().joint(JointAlignment.RIGHT_CENTER, image, self)
            case JointAlignment.LEFT_BOTTOM:
                return ImageJointer().joint(JointAlignment.RIGHT_BOTTOM, image, self)

        offset = self.__calc_absolute_paste_pos(align, image)
        shift_to = self.__calc_shift(offset)
        paste_to = self.__calc_paste(offset)
        parts = tuple(self.__run_joint(image, shift_to, paste_to))
        return ImageJointer.__make_from_tuple(parts)

    def joint(
        self,
        align: JointAlignment,
        *images: Image.Image | Figure,
    ) -> ImageJointer:
        """
        Joint new images to right side or bottom repeatedly.
        There are no side effect.

        Args:
            align (JointAlignment): how to align image

            *images (Image.Image | Figure): images to joint

        Returns:
            ImageJointer: New instance of jointed image. Method chainable.
        """
        jointed = self
        for element in images:
            jointed = jointed.joint_single(align, element)
        return jointed

    def to_image(self):
        """
        Make Image.

        Returns:
            Image.Image: image
        """
        output = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        for part in self.__parts:
            part.draw(output)
        return output
