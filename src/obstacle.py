import pygame


class Obstacle:

    def __init__(self, width=7, height=10):
        self.width = width
        self.height = height

    def draw(self, surface: pygame.Surface, x, y) -> None:
        pygame.draw.rect(surface, (255, 255, 255), (x, y, self.width, self.height))