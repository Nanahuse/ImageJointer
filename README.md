# ImageJointer
```python
    from image_jointer import Aline, ImageJointer
    from PIL import Image
    
    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (100, 100), (0, 0, 255))

    jointed = (
        ImageJointer(red)
        .joint(green, Aline.SideCenter)
        .joint(
            ImageJointer(blue).joint(blue, Aline.SideCenter),
            Aline.DownLeft
        )
    )
    joint_img = jointed.to_image()
```

![simple](./doc/joint_simple.png)
```python
    from image_jointer import Aline, ImageJointer
    from PIL import Image    

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blank = Blank(50, 100)
    green = Image.new("RGBA", (100, 100), (0, 255, 0))

    jointed = (
        ImageJointer(red)
        .joint(blank, Aline.SideCenter)
        .joint(green, Aline.SideCenter)
    )
    joint_img = jointed.to_image()
```
![blank](./doc/joint_blank.png)

```python
    from image_jointer import Aline, ImageJointer
    from PIL import Image

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))

    jointed = ImageJointer(red).joint(blue, Aline.SideCenter)
    joint_img = jointed.to_image()
```
![side_center](./doc/joint_side_center.png)
