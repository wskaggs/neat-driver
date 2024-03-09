from src.sim_object import SimObject
from pyray import *


def test_get_and_set_size() -> None:
    init_size = Vector2(1, 2)
    obj = SimObject(init_size, "")

    assert vector2_equals(obj.get_size(), init_size)
    assert obj.get_width() == init_size.x
    assert obj.get_height() == init_size.y

    new_size = Vector2(0, 5)
    obj.set_size(new_size)

    assert vector2_equals(obj.get_size(), new_size)
    assert obj.get_width() == new_size.x
    assert obj.get_height() == new_size.y

    new_width = 3
    obj.set_width(new_width)

    assert obj.get_width() == new_width
    assert obj.get_height() == new_size.y

    new_height = 12
    obj.set_height(new_height)

    assert obj.get_width() == new_width
    assert obj.get_height() == new_height


def test_get_and_set_pos() -> None:
    obj = SimObject(Vector2(0, 0), "")

    assert vector2_equals(obj.get_position(), Vector2(0, 0))
    assert obj.get_x() == 0
    assert obj.get_y() == 0

    new_pos = Vector2(1, 2)
    obj.set_position(new_pos)

    assert vector2_equals(obj.get_position(), new_pos)
    assert obj.get_x() == new_pos.x
    assert obj.get_y() == new_pos.y

    new_x = 3
    obj.set_x(new_x)

    assert obj.get_x() == new_x
    assert obj.get_y() == new_pos.y

    new_y = 12
    obj.set_y(new_y)

    assert obj.get_x() == new_x
    assert obj.get_y() == new_y


def test_get_and_set_angle() -> None:
    obj = SimObject(Vector2(0, 0), "")

    assert obj.get_angle() == 0

    new_angle = 1.23
    obj.set_angle(new_angle)

    assert obj.get_angle() == new_angle
