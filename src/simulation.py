import pygame


class Simulation:
    """
    The top-level class representing the AI driver simulation
    """
    def get_virtual_size(self) -> tuple[int, int]:
        """
        Get the virtual size of the current scene.

        :return: the virtual (width, height) of the scene
        """
        # Just a square for now to test scaling of the virtual surface
        return 100, 100

    def update(self, delta_time: float) -> None:
        """
        Update this simulation

        :param delta_time: elapsed time since the last update in milliseconds
        """
        ...

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the simulation onto a surface

        :param surface: the surface to draw on
        """
        # This just draws a red rectangle on the entire surface
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, *self.get_virtual_size()))
