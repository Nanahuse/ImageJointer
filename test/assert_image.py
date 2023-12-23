from PIL import Image


def assert_image(image: Image.Image, expected_image: Image.Image, is_same: bool = True):
    assert (image.tobytes() == expected_image.tobytes()) == is_same
