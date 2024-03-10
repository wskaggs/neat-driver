from .driver_base import DriverBase
from pyray import *


class HumanDriver(DriverBase):
    """
    A driver that is controlled by a human player. Used for debugging purposes
    """
    def update(self, delta_time: float) -> None:
        """
        Update this driver

        :param delta_time: time since the last update in seconds
        """
        if is_key_down(KeyboardKey.KEY_LEFT):
            self.turn_left()
        if is_key_down(KeyboardKey.KEY_RIGHT):
            self.turn_right()

        if is_key_down(KeyboardKey.KEY_UP) and is_key_down(KeyboardKey.KEY_LEFT):
            self.press_gas(delta_time)
            self.turn_left()
        elif is_key_down(KeyboardKey.KEY_UP) and is_key_down(KeyboardKey.KEY_RIGHT):
            self.press_gas(delta_time)
            self.turn_right()
        elif is_key_down(KeyboardKey.KEY_UP):
            self.press_gas(delta_time)
            self.set_steering_angle(0)

        if is_key_down(KeyboardKey.KEY_DOWN):
            self.press_brake(delta_time)

        super().update(delta_time)
