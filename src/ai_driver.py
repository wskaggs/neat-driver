from pyray import *
from .driver_base import DriverBase
from .track import Track
import neat
import math


class AiDriver(DriverBase):
    """
    A driver that is controlled by the NEAT neural network
    """
    def __init__(self, track: Track, genome: neat.DefaultGenome, config: neat.Config) -> None:
        super().__init__(track)
        self._genome = genome
        self._genome.fitness = 0
        self._network = neat.nn.FeedForwardNetwork.create(genome, config)
        self._time_stagnant = 0

    def update(self, delta_time: float) -> None:
        """
        Update this driver

        :param delta_time: elapsed time since the last update in seconds
        """
        # No need to update this driver if it's currently off track (dead)
        if self.is_off_track():
            return

        # Keep track of the amount of time spent stagnant (some drivers haven't learned to press the gas)
        if self.get_speed() == 0:
            self._time_stagnant += delta_time
        else:
            self._time_stagnant = 0

        # If the car is currently off track or has been stagnant for too long, mark as dead
        if self._track.is_off_track(self.get_position()) or self._time_stagnant >= 2:
            self.set_off_track(True)
            self._genome.fitness *= 0.5
            return

        # Update the driver and the fitness of the genome
        prev_pos = self.get_position()
        super().update(delta_time)
        distance_traveled = vector2_length(vector2_subtract(self.get_position(), prev_pos))
        self._genome.fitness += distance_traveled

        # Calculate the inputs for neat
        inputs = [self.get_speed(), self.get_steering_angle()]

        pos = self.get_position()
        angle = self.get_angle()
        num_casts = 12
        fov = math.pi
        angle_delta = fov / num_casts

        for i in range(num_casts):
            ray_end = self._track.ray_collision(pos, angle - fov / 2 + i * angle_delta)
            inputs.append(vector2_length(vector2_subtract(ray_end, pos)))

        # Calculate the outputs of the network and take corresponding actions
        outputs = self._network.activate(inputs)

        if outputs[0] > 0.5:
            self.press_gas(delta_time)
        if outputs[1] > 0.5:
            self.press_gas(delta_time)
        if outputs[2] > 0.5:
            self.turn_left(delta_time)
        if outputs[3] > 0.5:
            self.turn_right(delta_time)

    def draw(self) -> None:
        """
        Draw this driver to the screen
        """
        if not self.is_off_track():
            super().draw()
