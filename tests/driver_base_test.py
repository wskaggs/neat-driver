from src.driver_base import DriverBase
from src.track import Track


def test_get_and_set_speed() -> None:
    track = Track()
    driver = DriverBase(track)

    assert driver.get_speed() == 0

    new_speed = 1.23
    driver.set_speed(new_speed)

    assert driver.get_speed() == new_speed


def test_get_and_set_steering_angle() -> None:
    track = Track()
    driver = DriverBase(track)

    assert driver.get_steering_angle() == 0

    new_steering_angle = driver.MAX_STEERING_ANGLE / 2
    driver.set_steering_angle(new_steering_angle)

    assert driver.get_steering_angle() == new_steering_angle

    new_steering_angle = -driver.MAX_STEERING_ANGLE - 1
    driver.set_steering_angle(new_steering_angle)

    assert driver.get_steering_angle() == -driver.MAX_STEERING_ANGLE

    new_steering_angle = driver.MAX_STEERING_ANGLE + 1
    driver.set_steering_angle(new_steering_angle)

    assert driver.get_steering_angle() == driver.MAX_STEERING_ANGLE
