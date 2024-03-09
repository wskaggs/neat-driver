from pyray import *
from src import Simulation, TexturePack


def main() -> None:
    """
    Entry point into running the simulation visualization
    """
    # Initialize raylib and the opengl context
    init_window(800, 600, "NEAT Driver")

    # Ensure initialization was successful
    if not is_window_ready():
        raise RuntimeError("[ERROR]: Failed to initialize the window")

    # Configure the window
    set_window_state(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    set_target_fps(60)

    # Load all image assets
    TexturePack.load_all("assets/images/")

    # Run the game loop
    simulation = Simulation()

    while not window_should_close():
        # Update the simulation
        simulation.update(get_frame_time())

        # Draw the simulation to the screen
        begin_drawing()
        clear_background(BLACK)
        simulation.draw()
        end_drawing()

    # De-initialize and close the window
    TexturePack.unload_all()
    close_window()


if __name__ == "__main__":
    main()
