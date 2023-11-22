from enum import Enum, auto


class JointAlign(Enum):
    # 元画像の右側に連結する。
    SIDE_TOP = auto()  # 上端ぞろえ
    SIDE_CENTER = auto()  # 中心ぞろえ
    SIDE_BOTTOM = auto()  # 下端ぞろえ
    # 元画像の下側に連結する。
    UNDER_LEFT = auto()  # 左端ぞろえ
    UNDER_CENTER = auto()  # 中心ぞろえ
    UNDER_RIGHT = auto()  # 右端ぞろえ


class PositionAlign(Enum):
    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    CENTER_LEFT = auto()
    CENTER_CENTER = auto()
    CENTER_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()
