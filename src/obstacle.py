import pygame

class Obstacle:

    def __init__(self, width=7, height=10):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def draw(self, surface: pygame.Surface, x, y) -> None:
        pygame.draw.rect(surface, (0, 0, 0), self.rect.move(x, y))

    def didCollide(self, other: pygame.Rect) -> bool:
        # This is if our car polygon is a rectangle, otherwise we can use collidepoint
        return self.rect.colliderect(other)
