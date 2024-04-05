from pyray import *
from .sim_object import SimObject
from .obstacle_base import ObstacleBase
from .texture_pack import TexturePack
from xml.etree.ElementTree import Element
from math import radians, sin, cos, inf


class Track(SimObject):
    """
    Class to represent a track, its valid play area, and its checkpoints
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self._map = None
        self._driver_start_pos = Vector2(0, 0)
        self._driver_start_angle = 0
        self._obstacles = []

        # TODO: move the checkpoints to an xml file (these are for the oval track)
        self._checkpoints = [] #[(Vector2(50, 75), Vector2(150, 75))]

        # TODO: move this obstacle to an xml file (this is for the oval track)
        #obstacle = ObstacleBase(Vector2(7, 7), "box.png")
        #obstacle.set_position(Vector2(100, 72))
        #self._obstacles.append(obstacle)

    def get_driver_start_pos(self) -> Vector2:
        """
        Get the starting position for drivers

        :return: the starting driver position in meters
        """
        return self._driver_start_pos

    def set_driver_start_pos(self, start_pos: Vector2) -> None:
        """
        Set the driver starting position

        :param start_pos: the starting driver position in meters
        """
        self._driver_start_pos = start_pos

    def get_driver_start_x(self) -> float:
        """
        Get the x position where a driver should start

        :return: the x component of the driver's start position in meters
        """
        return self._driver_start_pos.x

    def set_driver_start_x(self, x: float) -> None:
        """
        Set the x component of the driver's start position

        :param x: the new x component in meters
        """
        self._driver_start_pos.x = x

    def get_driver_start_y(self) -> float:
        """
        Get the y position where a driver should start

        :return: the y component of the driver's starting position in meters
        """
        return self._driver_start_pos.y

    def set_driver_start_y(self, y: float) -> None:
        """
        Set the y component of the driver's starting position

        :param y: the y component of the driver's starting position in meters
        """
        self._driver_start_pos.y = y

    def get_driver_start_angle(self) -> float:
        """
        Get the angle that drivers should start at

        :return: the start angle of the drivers in radians
        """
        return self._driver_start_angle

    def set_driver_start_angle(self, angle: float) -> None:
        """
        Set the angle that drivers should start at

        :param angle: the start angle of the drivers in radians
        """
        self._driver_start_angle = angle

    def xml_load(self, node: Element) -> None:
        """
        Load attributes about this track from a xml node

        :param node: the node to load from
        """
        super().xml_load(node)

        # Load attributes about where to initially place the drivers
        if (start_x := node.get("start_x")) is not None:
            self._driver_start_pos.x = float(start_x)
        if (start_y := node.get("start_y")) is not None:
            self._driver_start_pos.y = float(start_y)

        # Load attributes about the driver's initial heading (NOTE: the xml is in degrees, internally stored as radians)
        if (start_angle := node.get("start_angle")) is not None:
            self._driver_start_angle = radians(float(start_angle))

        # Load the map (used for valid placement)
        if (map_filename := node.get("map")) is not None:
            map_image = TexturePack.get_image(map_filename)

            if map_image is not None:
                self._map = map_image

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

    def is_off_track(self, pos: Vector2) -> bool:
        """
        Check if a position is off the track

        :param pos: the position to check for in world space
        :return: `True` if the position is off the track, `False` otherwise
        """
        map_coord = self._world_to_map(pos)
        pixel_x = int(map_coord.x)
        pixel_y = int(map_coord.y)

        if pixel_x < 0 or pixel_x >= self._map.width or pixel_y < 0 or pixel_y >= self._map.height:
            return True

        return get_image_color(self._map, pixel_x, pixel_y).a == 0

    def ray_collision(self, pos: Vector2, angle: float) -> Vector2:
        """
        Cast a ray and determine the intersection with the edge of the track or an obstacle

        DDA algorithm: https://lodev.org/cgtutor/raycasting.html

        :param pos: the position to start the ray
        :param angle: the angle/heading of the ray
        :return: the distance until a collision with a track edge/obstacle
        """
        # Based on the heading, calculate the distance to travel between x and y pixel sides in map space
        heading = Vector2(cos(angle), sin(angle))
        delta_dist_x = inf if heading.x == 0 else abs(1 / heading.x)
        delta_dist_y = inf if heading.y == 0 else abs(1 / heading.y)

        # Calculate where we are within the map space and the corresponding pixel indices
        map_pos = self._world_to_map(pos)
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
            current_world_coord = self._map_to_world(vector2_add(map_pos, vector2_scale(heading, distance)))

            for obstacle in self._obstacles:
                if obstacle.hit_test(current_world_coord):
                    found_end = True
                    break

        return pos if not found_end else self._map_to_world(vector2_add(map_pos, vector2_scale(heading, distance)))
    
    def checkpoint_check(self, car_pos: Vector2, new_pos: Vector2) -> bool:
        """
        Check if car passed checkpoint

        :param car_pos: position of the car
        :param new_pos: new position of car
        :return: True if a checkpoint is crossed
        """
        for checkpoint in self._checkpoints:
            start, end = checkpoint

            # There is an edge case when the end position of a car will be directly on this line
            # Realistically, this shouldn't be a problem and can probably be ignored
            if check_collision_lines(car_pos, new_pos, start, end, None):
                return True

        return False
