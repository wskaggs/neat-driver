from pyray import *
from .track import Track
from .human_driver import HumanDriver
from .sim_object import SimObject


class Simulation:
    """
    The top-level class representing the AI driver simulation
    """
    def __init__(self):
        """
        Constructor
        """
        self._track = Track()
        self._update_scene_fitment()

        # TODO: figure out a better way to create drivers and obstacles. Xml file?
        self.driver = HumanDriver()
        self.obstacle = SimObject(Vector2(5, 5), "box.png")
        self.obstacle.set_position(Vector2(100, 75))

    def update(self, delta_time: float) -> None:
        """
        Update this simulation

        :param delta_time: elapsed time since the last update in seconds
        """
        self.driver.update(delta_time)

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
        self.driver.draw()
        self.obstacle.draw()

        # Restore the view matrix
        rl_pop_matrix()
