from PIL import Image, ImageChops


def assert_image(image: Image.Image, expected_image: Image.Image):
    diff = ImageChops.difference(image, expected_image)

    assert diff.getbbox() is None
