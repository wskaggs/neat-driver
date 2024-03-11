from pyray import *
from .sim_object import SimObject
from .obstacle_base import ObstacleBase
from .texture_pack import TexturePack
import math


class Track(SimObject):
    """
    Class to represent a track, its valid play area, and its checkpoints
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(Vector2(200, 100), "oval_track.png")
        self._map = TexturePack.get_image("oval_track_valid.png")
        self._obstacles = []

        # TODO: remove this hard-coded obstacle
        obstacle = ObstacleBase(Vector2(5, 5), "box.png")
        obstacle.set_position(Vector2(100, 75))
        self._obstacles.append(obstacle)

    def draw(self) -> None:
        """
        Draw this track to the screen
        """
        # Base class draws images centered at their position, we need to draw the top-left at its position
        half_size = vector2_scale(self.get_size(), 0.5)

        rl_push_matrix()
        rl_translatef(half_size.x, half_size.y, 0)
        super().draw()
        rl_pop_matrix()

        # Draw all the obstacles
        for obstacle in self._obstacles:
            obstacle.draw()

    def _world_to_map(self, pos: Vector2) -> Vector2:
        """
        Convenience function to convert a world-space position into the corresponding map coordinate

        :param pos: the world space position
        :return: the map coordinate
        """
        return Vector2(pos.x / self._size.x * self._map.width, pos.y / self._size.y * self._map.height)

    def _map_to_world(self, pos: Vector2) -> Vector2:
        """
        Convenience function to convert a map-space position into the corresponding world-space coordinate

        :param pos: the map-space position
        :return: the world coordinate
        """
        return Vector2(pos.x / self._map.width * self._size.x, pos.y / self._map.height * self._size.y)

    def ray_collision(self, world_pos: Vector2, angle: float) -> Vector2:
        """
        Cast a ray and determine the intersection with the edge of the track or an obstacle

        DDA algorithm: https://lodev.org/cgtutor/raycasting.html

        :param world_pos: the position to start the ray
        :param angle: the angle/heading of the ray
        :return: the distance until a collision with a track edge/obstacle
        """
        # Based on the heading, calculate the distance to travel between x and y pixel sides in map space
        heading = Vector2(math.cos(angle), math.sin(angle))
        delta_dist_x = math.inf if heading.x == 0 else abs(1 / heading.x)
        delta_dist_y = math.inf if heading.y == 0 else abs(1 / heading.y)

        # Calculate where we are within the map space and the corresponding pixel indices
        map_pos = self._world_to_map(world_pos)
        pixel_x = int(map_pos.x)
        pixel_y = int(map_pos.y)

        # Calculate the initial step to the next x or y side based on the heading
        side_dist_x = ((map_pos.x - pixel_x) if heading.x < 0 else (pixel_x + 1 - map_pos.x)) * delta_dist_x
        side_dist_y = ((map_pos.y - pixel_y) if heading.y < 0 else (pixel_y + 1 - map_pos.y)) * delta_dist_y

        # Calculate the step between pixels based on the heading
        step_x = -1 if heading.x < 0 else 1
        step_y = -1 if heading.y < 0 else 1

        # Cast the ray until we reach an obstacle or an edge of the track
        found_end = False
        distance = 0

        while not found_end:
            # Move to the next x or y boundary, whichever is closer
            if side_dist_x < side_dist_y:
                distance = side_dist_x
                side_dist_x += delta_dist_x
                pixel_x += step_x
            else:
                distance = side_dist_y
                side_dist_y += delta_dist_y
                pixel_y += step_y

            # If we are outside the map, we can terminate the cast
            if pixel_x < 0 or pixel_x >= self._map.width or pixel_y < 0 or pixel_y >= self._map.height:
                break

            # Otherwise, we can terminate the cast if we hit an invalid (transparent) location
            if get_image_color(self._map, pixel_x, pixel_y).a == 0:
                found_end = True
                break

            # If we are still in a valid track location, check for collision with any obstacles
            current_world_cord = self._map_to_world(vector2_add(map_pos, vector2_scale(heading, distance)))

            for obstacle in self._obstacles:
                if obstacle.hit_test(current_world_cord):
                    found_end = True
                    break

        return None if not found_end else self._map_to_world(vector2_add(map_pos, vector2_scale(heading, distance)))
