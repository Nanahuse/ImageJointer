from __future__ import annotations

from PIL import Image

from .base.blank import Blank
from .base.enums import JointAlign, PositionAlign
from .base.figure import Figure
from .image_jointer import ImageJointer


class Utility(object):
    def __init__(
        self,
    ):
        raise NotImplementedError("Cannot construct")

    @staticmethod
    def unify_image_size(align: PositionAlign, *images: Image.Image | Figure):
        """
        All image will be unified to maximum width and heigh.
        Add transparent padding if image width (height) is smaller then maximum width (height).

        Args:
            align (PositionAlign): how to add transparent padding
            *images (Image.Image | Figure): images to joint

        Returns:
            tuple[ImageJointer]: tuple of adjusted image
        """
        width = max(element.width for element in images)
        height = max(element.height for element in images)

        match align:
            case PositionAlign.TOP_LEFT:
                height_align = JointAlign.SIDE_TOP
                width_align = JointAlign.UNDER_LEFT
            case PositionAlign.TOP_CENTER:
                height_align = JointAlign.SIDE_TOP
                width_align = JointAlign.UNDER_CENTER
            case PositionAlign.TOP_RIGHT:
                height_align = JointAlign.SIDE_TOP
                width_align = JointAlign.UNDER_RIGHT
            case PositionAlign.CENTER_LEFT:
                height_align = JointAlign.SIDE_CENTER
                width_align = JointAlign.UNDER_LEFT
            case PositionAlign.CENTER_CENTER:
                height_align = JointAlign.SIDE_CENTER
                width_align = JointAlign.UNDER_CENTER
            case PositionAlign.CENTER_RIGHT:
                height_align = JointAlign.SIDE_CENTER
                width_align = JointAlign.UNDER_RIGHT
            case PositionAlign.BOTTOM_LEFT:
                height_align = JointAlign.SIDE_BOTTOM
                width_align = JointAlign.UNDER_LEFT
            case PositionAlign.BOTTOM_CENTER:
                height_align = JointAlign.SIDE_BOTTOM
                width_align = JointAlign.UNDER_CENTER
            case PositionAlign.BOTTOM_RIGHT:
                height_align = JointAlign.SIDE_BOTTOM
                width_align = JointAlign.UNDER_RIGHT

        return tuple(
            ImageJointer(Blank(0, height)).joint(height_align, element).joint(width_align, Blank(width, 0))
            for element in images
        )
