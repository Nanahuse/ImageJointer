# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from pathlib import Path

IMAGE_FOLDER = Path("./test/image/")


def test_vector():
    from image_jointer import Vector

    assert Vector(5, 5) + Vector(6, 6) == Vector(11, 11)


def test_joint_simple():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (100, 100), (0, 0, 255))

    jointed = (
        ImageJointer(red)
        .joint(green, JointAlign.SIDE_CENTER)
        .joint(ImageJointer(blue).joint(blue, JointAlign.SIDE_CENTER), JointAlign.UNDER_LEFT)
    )
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_simple_tmp.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 0:100, 0] = 255
    correct_array[0:100, 100:200, 1] = 255
    correct_array[100:200, 0:200, 2] = 255
    correct_array[:, :, 3] = 255
    # 正解画像の保存
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_simple_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_side_top():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.SIDE_TOP)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_side_top.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 0:100, 0] = 255
    correct_array[0:100, 0:100, 3] = 255
    correct_array[0:200, 100:200, 2] = 255
    correct_array[0:200, 100:200, 3] = 255
    # 正解画像の保存
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_side_top_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_side_center():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.SIDE_CENTER)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_side_center.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[50:150, 0:100, 0] = 255
    correct_array[50:150, 0:100, 3] = 255
    correct_array[0:200, 100:200, 2] = 255
    correct_array[0:200, 100:200, 3] = 255
    # 正解画像の保存
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_side_center_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_side_bottom():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.SIDE_BOTTOM)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_side_bottom.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[100:200, 0:100, 0] = 255
    correct_array[100:200, 0:100, 3] = 255
    correct_array[0:200, 100:200, 2] = 255
    correct_array[0:200, 100:200, 3] = 255
    # 正解画像の保存
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_side_bottom_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_down_left():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (200, 100), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.UNDER_LEFT)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_down_left.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 0:100, 0] = 255
    correct_array[0:100, 0:100, 3] = 255
    correct_array[100:200, 0:200, 2] = 255
    correct_array[100:200, 0:200, 3] = 255
    # 正解画像の保存
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_down_left_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_down_center():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (200, 100), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.UNDER_CENTER)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_down_center.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 50:150, 0] = 255
    correct_array[0:100, 50:150, 3] = 255
    correct_array[100:200, 0:200, 2] = 255
    correct_array[100:200, 0:200, 3] = 255
    # 正解画像の保存
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_down_center_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_joint_down_right():
    from image_jointer import JointAlign, ImageJointer
    from PIL import Image
    import numpy as np

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (200, 100), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, JointAlign.UNDER_RIGHT)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_down_right.png")

    correct_array = np.zeros((200, 200, 4), dtype=np.uint8)
    correct_array[0:100, 100:200, 0] = 255
    correct_array[0:100, 100:200, 3] = 255
    correct_array[100:200, 0:200, 2] = 255
    correct_array[100:200, 0:200, 3] = 255
    # 正解画像の保存
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_down_right_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)


def test_blank():
    from image_jointer import JointAlign, ImageJointer, Blank
    from PIL import Image
    import numpy as np

    red = Image.new("RGB", (100, 100), (255, 0, 0))
    blank = Blank(50, 100)
    green = Image.new("RGB", (100, 100), (0, 255, 0))

    jointed = ImageJointer(red).joint(blank, JointAlign.SIDE_CENTER).joint(green, JointAlign.SIDE_CENTER)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint_blank_tmp.png")

    correct_array = np.zeros((100, 250, 4), dtype=np.uint8)
    correct_array[0:100, 0:100, 0] = 255
    correct_array[0:100, 0:100, 3] = 255
    correct_array[0:100, 150:250, 1] = 255
    correct_array[0:100, 150:250, 3] = 255
    Image.fromarray(correct_array).save(IMAGE_FOLDER / "joint_blank_correct.png")

    assert np.array_equal(np.asarray(joint_img), correct_array)
