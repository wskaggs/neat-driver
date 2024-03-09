from pyray import *
from .texture_pack import TexturePack
from . import consts


class SimObject:
    """
    The base class for all simulation objects
    """
    def __init__(self, size: Vector2, texture_filename: str) -> None:
        """
        Constructor

        :param size: the size of this object in meters
        :param texture_filename: the filename of the texture for this object
        """
        self._texture = TexturePack.get_texture(texture_filename)
        self._size = size
        self._pos = Vector2(0, 0)
        self._angle = 0

    def get_size(self) -> Vector2:
        """
        Get the size of this object

        :return: the (width, height) of this object in meters
        """
        return self._size

    def set_size(self, size: Vector2) -> None:
        """
        Set the size of this object

        :param size: the (width, height) of this object in meters
        """
        self._size = size

    def get_width(self) -> float:
        """
        Get the width of this object

        :return: the width of this object in meters
        """
        return self._size.x

    def set_width(self, width: float) -> None:
        """
        Set the width of this object

        :param width: the new width of this object in meters
        """
        self._size.x = width

    def get_height(self) -> float:
        """
        Get the height of this object

        :return: the height of this object in meters
        """
        return self._size.y

    def set_height(self, height: float) -> None:
        """
        Set the height of this object

        :param height: the new height of this object in meters
        """
        self._size.y = height

    def get_position(self) -> Vector2:
        """
        Get the position of this object

        :return: the (x, y) position of this object in meters
        """
        return self._pos

    def set_position(self, pos: Vector2) -> None:
        """
        Set the position of this object

        :param pos: the new (x, y) position of this object in meters
        """
        self._pos = pos

    def get_x(self) -> float:
        """
        Get the x position of this object

        :return: the x position of this object in meters
        """
        return self._pos.x

    def set_x(self, x: float) -> None:
        """
        Set the x position of this object

        :param x: the new x position in meters
        """
        self._pos.x = x

    def get_y(self) -> float:
        """
        Get the y position of this object

        :return: the y position of this object in meters
        """
        return self._pos.y

    def set_y(self, y: float) -> None:
        """
        Set the y position of this object

        :param y: the new x position in meters
        """
        self._pos.y = y

    def get_angle(self) -> float:
        """
        Get the angle/rotation of this object

        :return: the angle in radians
        """
        return self._angle

    def set_angle(self, angle: float) -> None:
        """
        Set the angle/rotation of this object

        :param angle: the new angle in radians
        """
        self._angle = angle

    def update(self, delta_time: float) -> None:
        """
        Update this object

        :param delta_time: the elapsed time since the last update in seconds
        """
        pass

    def draw(self) -> None:
        """
        Draw this object to the screen
        """
        # Save the current state of the view matrix
        rl_push_matrix()

        # Move to the center of this object and rotate for its orientation
        rl_translatef(self._pos.x, self._pos.y, 0)
        rl_rotatef(consts.RAD_TO_DEG * self._angle, 0, 0, 1)

        # Draw the texture to the screen
        source_rect = Rectangle(0, 0, self._texture.width, self._texture.height)
        dest_rect = Rectangle(-self._size.x / 2, -self._size.y / 2, self._size.x, self._size.y)
        draw_texture_pro(self._texture, source_rect, dest_rect, Vector2(0, 0), 0, WHITE)

        # Restore the view matrix
        rl_pop_matrix()
