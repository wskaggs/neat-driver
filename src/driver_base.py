from pyray import *
from .sim_object import SimObject
from .track import Track
import math


class DriverBase(SimObject):
	"""
	The base class for a driver
	"""
	MAX_STEERING_ANGLE = math.pi / 3
	STEERING_RATE = math.radians(90)
	FRICTION = 0.9
	DRAG = 0.001
	HORSEPOWER = 40
	BRAKE_POWER = 30

	def __init__(self, track: Track) -> None:
		"""
		Constructor
		"""
		super().__init__(Vector2(5.5, 2), "car.png")
		self._track = track
		self._speed = 0
		self._steering_angle = 0
		self._off_tack = False

	def get_speed(self) -> float:
		"""
		Get the speed of this driver

		:return: the speed in meters/second
		"""
		return self._speed

	def set_speed(self, speed: float) -> None:
		"""
		Set the speed of this driver

		:param speed: the new speed in meters/second
		"""
		self._speed = speed

	def get_steering_angle(self) -> float:
		"""
		Get the steering angle of this driver

		:return: the steering angle in radians
		"""
		return self._steering_angle

	def set_steering_angle(self, steering_angle: float) -> None:
		"""
		Set the steering angle of this driver

		The steering angle is bounded between [-MAX_STEERING_ANGLE, MAX_STEERING_ANGLE]

		:param steering_angle: the new steering angle in radians
		"""
		self._steering_angle = max(-self.MAX_STEERING_ANGLE, min(steering_angle, self.MAX_STEERING_ANGLE))

	def is_off_track(self) -> bool:
		"""
		Check if this driver is currently off the track

		:return: `True` if the driver is off the track, `False` otherwise
		"""
		return self._off_tack

	def set_off_track(self, off_track: bool) -> None:
		"""
		Set the flag indicating if this driver is off track

		:param off_track: the new off track flag
		"""
		self._off_tack = off_track

	def turn_left(self, delta_time: float) -> None:
		"""
		Turn to the left by one tick

		:param delta_time: the elapsed time since the last update in seconds
		"""
		self.set_steering_angle(self.get_steering_angle() - self.STEERING_RATE * delta_time)

	def turn_right(self, delta_time: float) -> None:
		"""
		Turn to the left by one tick

		:param delta_time: the elapsed time since the last update in seconds
		"""
		self.set_steering_angle(self.get_steering_angle() + self.STEERING_RATE * delta_time)

	def press_gas(self, delta_time: float) -> None:
		"""
		Accelerate using the gas pedal

		:param delta_time: the elapsed time since the last update in seconds
		"""
		self._speed += self.HORSEPOWER * delta_time

	def press_brake(self, delta_time: float) -> None:
		"""
		Decelerate using the brake pedal

		:param delta_time: the elapsed time since the last update in seconds
		"""
		self._speed = max(0.0, self._speed - self.BRAKE_POWER * delta_time)

	def _apply_steering(self, delta_time: float) -> None:
		"""
		Apply the steering forces to the driver

		:param delta_time: the elapsed time since the last update in seconds
		"""
		# Calculate the heading based on the current angle
		heading = Vector2(math.cos(self.get_angle()), math.sin(self.get_angle()))

		# Calculate the current location of the front and back wheels
		wheel_delta = vector2_scale(heading, self.get_width() / 2)
		front_wheel = vector2_add(self.get_position(), wheel_delta)
		rear_wheel = vector2_subtract(self.get_position(), wheel_delta)

		# Move the two wheels forward based on their respective headings
		steering_heading = vector2_rotate(heading, self._steering_angle)
		front_wheel = vector2_add(front_wheel, vector2_scale(steering_heading, self._speed * delta_time))
		rear_wheel = vector2_add(rear_wheel, vector2_scale(heading, self._speed * delta_time))

		# Adjust the steering angle based on the change of the car's heading
		new_angle = math.atan2(front_wheel.y - rear_wheel.y, front_wheel.x - rear_wheel.x)
		self.set_steering_angle(self.get_steering_angle() - (new_angle - self.get_angle()))

		# Update the position and angle
		self.set_position(vector2_scale(vector2_add(front_wheel, rear_wheel), 0.5))
		self.set_angle(new_angle)

	def _apply_friction(self, delta_time: float) -> None:
		"""
		Apply friction forces to the driver

		:param delta_time: the elapsed time since the last update in seconds
		"""
		if self._speed <= 0.1:
			self._speed = 0
			return

		rolling_friction = self.FRICTION * self._speed
		drag = self.DRAG * self._speed ** 2
		self._speed -= (rolling_friction + drag) * delta_time

	def update(self, delta_time: float) -> None:
		"""
		Update this driver

		:param delta_time: the elapsed time since the last update in seconds
		"""
		self._apply_friction(delta_time)
		self._apply_steering(delta_time)
