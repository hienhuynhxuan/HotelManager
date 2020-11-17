import enum


class Status(enum.Enum):
    ThereIsRoom = "Trống"
    OutOfRoom = "Đang dùng"


class Role(enum.Enum):
    admin = "Quản trị viên"
    user = "Lễ Tân"



