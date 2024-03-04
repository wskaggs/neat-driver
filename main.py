import pygame
import math
from src import Simulation, Obstacle


def main() -> None:
    """
    Entry point into running the simulation visualization
    """

    # Initialize pygame and the window
    pygame.init()
    pygame.display.set_caption("NEAT Driver")
    window = pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Run the game loop
    simulation = Simulation()
    obstacle = Obstacle()
    window_should_close = False
    delta_time = 0

    #colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    track = [
        (150, 100),
        (650, 100),
        (650, 500),
        (150, 500),
        (150, 100)
    ]

    while not window_should_close:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_should_close = True

        # Update the simulation
        simulation.update(delta_time)

        # Create the virtual surface and draw the simulation on this surface
        surface = pygame.Surface(simulation.get_virtual_size())
        simulation.draw(surface)
        obstacle.draw(surface, 50, 50)

        # Draw the virtual surface onto the main surface (centered, scaled using aspect-fit)
        scale = min(window.get_width() / surface.get_width(), window.get_height() / surface.get_height())
        dest_width = scale * surface.get_width()
        dest_height = scale * surface.get_height()
        offset_x = (window.get_width() - dest_width) / 2
        offset_y = (window.get_height() - dest_height) / 2
        window.fill((0, 0, 0))
        window.blit(pygame.transform.scale(surface, (dest_width, dest_height)), (offset_x, offset_y))

        #draw track
        pygame.draw.rect(window, black, pygame.Rect(120, 50, 560, 60))
        pygame.draw.rect(window, black, pygame.Rect(120, 50, 60, 500))
        pygame.draw.rect(window, black, pygame.Rect(120, 500, 560, 60))
        pygame.draw.rect(window, black, pygame.Rect(620, 50, 60, 500))

        # Update the screen buffer and limit the framerate
        pygame.display.flip()
        delta_time = clock.tick(60)

    # De-initialize and close the window
    pygame.quit()


if __name__ == "__main__":
    main()
