from pyray import *
from src import Simulation, TexturePack, AiDriver
import neat
import sys
import os


def initialize_window() -> None:
    """
    Convenience function to initialize/configure raylib and load all necessary assets
    """
    # Initialize raylib and ensure initialization was successful
    init_window(800, 600, "NEAT Driver")

    if not is_window_ready():
        raise RuntimeError("[ERROR]: Failed to initialize the window")

    # Configure the window
    set_window_state(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    set_target_fps(60)

    # Load all image assets
    TexturePack.load_all("assets/images/")


def terminate_window() -> None:
    """
    Convenience function to terminate the raylib window and unload all loaded assets
    """
    TexturePack.unload_all()
    close_window()


def load_population_from_config_file(path: str, checkpoint_save_path: str | None) -> neat.Population:
    """
    Create a population given the path to the neat configuration file

    :param path: path to the neat configuration file
    :param checkpoint_save_path: path to save checkpoints to
    :return: the created population
    """
    # Load the configuration file
    neat_types = (neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation)
    config = neat.Config(*neat_types, path)

    # Create the population and add reporters for debugging
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if checkpoint_save_path is not None:
        if not os.path.exists(checkpoint_save_path):
            os.makedirs(checkpoint_save_path)

        checkpointer = neat.Checkpointer(5, None, f"{checkpoint_save_path}/neat-checkpoint-")
        population.add_reporter(checkpointer)

    return population


def load_population_from_checkpoint(checkpoint_path: str) -> neat.Population:
    """
    Load a population from a saved checkpoint

    :param checkpoint_path: the path to the saved checkpoint
    :return: the created population
    """
    population = neat.Checkpointer.restore_checkpoint(checkpoint_path)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(5, None, f"{os.path.dirname(checkpoint_path)}/neat-checkpoint-"))

    return population


def run_simulation(population: neat.Population, track_filepath: str, tick_time: float = 1 / 20) -> None:
    """
    Run the driving simulation and train the population of drivers

    :param population: the population to train
    :param track_filepath: path to the xml file describing the track to use
    :param tick_time: the time between updates in seconds
    """
    simulation = Simulation()
    simulation.xml_load(track_filepath)

    def evaluate_genomes(genomes: list[tuple[int, neat.DefaultGenome]], config: neat.Config) -> None:
        """
        Inner function to evaluate the current generation of drivers

        :param genomes: the (genome_id, genome) for each individual of the population
        :param config: the current neat configuration
        """
        # Purge all current drivers and create the next generation
        simulation.purge_drivers()

        for genome_id, genome in genomes:
            driver = AiDriver(simulation.get_track(), genome, config)
            simulation.add_driver(driver)

        # Run the simulation until all drivers are off-track or the
        time_since_start = 0
        time_since_last_update = 0

        while time_since_start < 60 and not simulation.all_drivers_off_track():
            # Close the window gracefully if requested by the user
            if window_should_close():
                terminate_window()
                sys.exit()

            # Update the drivers (we may need to do this multiple times depending on the frame rate)
            time_since_start += get_frame_time()
            time_since_last_update += get_frame_time()

            while time_since_last_update >= tick_time:
                simulation.update(tick_time)
                time_since_last_update -= tick_time

            # Update the visualization
            begin_drawing()
            clear_background(BLACK)
            simulation.draw()
            end_drawing()

        # Add a bonus to the drivers that are still alive after the alotted time ends
        for driver in simulation._drivers:
            if isinstance(driver, AiDriver) and not driver.is_off_track():
                driver._genome.fitness *= 1.2

    # Train the population
    population.run(evaluate_genomes)


def main() -> None:
    """
    Entry point into running the simulation visualization
    """
    initialize_window()

    # Load the population from a configuration file
    config_filepath = "assets/configs/config-feedforward.txt"
    checkpoint_save_path = "assets/checkpoints/oval"
    population = load_population_from_config_file(config_filepath, checkpoint_save_path)

    # Load the population from a checkpoint
    #population = load_population_from_checkpoint("assets/checkpoints/windy/neat-checkpoint-59")

    run_simulation(population, "assets/tracks/oval.xml")
    terminate_window()


if __name__ == "__main__":
    main()
