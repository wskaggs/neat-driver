from pyray import *
from .track import Track
from .driver_base import DriverBase
import math


class Simulation:
    """
    The top-level class representing the AI driver simulation
    """
    def __init__(self) -> None:
        """
        Constructor
        """
        self._track = Track()
        self._update_scene_fitment()
        self._drivers = []

    def get_track(self) -> Track:
        """
        Get the currently loaded track

        :return: the current track
        """
        return self._track

    def add_driver(self, driver: DriverBase) -> None:
        """
        Add a driver to the simulation and place it at the track start

        :param driver: the driver to add
        """
        driver.set_position(Vector2(214, 94))
        driver.set_angle(math.pi * 3 / 4)
        self._drivers.append(driver)

    def purge_drivers(self) -> None:
        """
        Clear all drivers currently on the track
        """
        self._drivers.clear()

    def all_drivers_off_track(self) -> bool:
        """
        Check if all drivers are currently off the track

        :return: `True` if all drivers are off the track, `False` otherwise
        """
        for driver in self._drivers:
            if not driver.is_off_track():
                return False

        return True

    def update(self, delta_time: float) -> None:
        """
        Update this simulation

        :param delta_time: elapsed time since the last update in seconds
        """
        for driver in self._drivers:
            initial_position = driver.get_position()
            driver.update(delta_time)
            new_position = driver.get_position()

            if self._track.checkpoint_check(initial_position, new_position):
                print('checkpoint passed')

    def _update_scene_fitment(self) -> None:
        """
        Convenience function to update the fitment of the virtual scene
        """
        screen_size = Vector2(get_screen_width(), get_screen_height())
        scene_size = self._track.get_size()

        self._scale = min(screen_size.x / scene_size.x, screen_size.y / scene_size.y)
        dest_size = vector2_scale(scene_size, self._scale)
        self._offset = vector2_scale(vector2_subtract(screen_size, dest_size), 0.5)

    def draw(self) -> None:
        """
        Draw the simulation
        """
        # Update the fitment of the scene if needed
        if is_window_resized():
            self._update_scene_fitment()

        # Save the current view matrix
        rl_push_matrix()

        # Translate and scale for the virtual coordinate system
        rl_translatef(self._offset.x, self._offset.y, 0)
        rl_scalef(self._scale, self._scale, 1)

        # Draw simulation objects
        self._track.draw()

        for driver in self._drivers:
            driver.draw()

        # Restore the view matrix
        rl_pop_matrix()
