from pyray import *
from .sim_object import SimObject
from .texture_pack import TexturePack


class ObstacleBase(SimObject):
    """
    The base class for all obstacles
    """
    def __init__(self, size: Vector2, texture_filename: str) -> None:
        """
        Constructor
        """
        super().__init__(size, texture_filename)
        self._image = TexturePack.get_image(texture_filename)

    def hit_test(self, point: Vector2) -> bool:
        """
        Check if a point is contained in this object

        :param point: the point to check
        :return: `True` if the point is contained in this obstacle, `False` otherwise
        """
        # Calculate the offset from this obstacle's center, aligned with this obstacle's orientation
        offset = vector2_rotate(vector2_subtract(point, self.get_position()), -self.get_angle())

        # Calculate the coordinates of the corresponding pixel within the image
        size = self.get_size()
        pixel_x = int(self._image.width * (0.5 + offset.x / size.x))
        pixel_y = int(self._image.height * (0.5 + offset.y / size.y))

        # If the pixel is not a valid location, it's not a hit
        if pixel_x < 0 or pixel_x >= self._image.width or pixel_y < 0 or pixel_y >= self._image.height:
            return False

        # Otherwise, check that the pixel is not transparent
        return get_image_color(self._image, pixel_x, pixel_y).a != 0
