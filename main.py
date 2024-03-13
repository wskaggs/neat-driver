from pyray import *
from src import Simulation, TexturePack, AiDriver
import neat
import sys


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


def load_population_from_config_file(path: str) -> neat.Population:
    """
    Create a population given the path to the neat configuration file

    :param path: path to the neat configuration file
    :return: the created population
    """
    # Load the configuration file
    neat_types = (neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation)
    config = neat.Config(*neat_types, path)

    # Create the population and add reporters for debugging
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    return population


def run_simulation(population: neat.Population) -> None:
    """
    Run the driving simulation and train the population of drivers
    """
    simulation = Simulation()

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

        # Run the simulation until all drivers are off-track
        while not simulation.all_drivers_off_track():
            # Close the window gracefully if requested by the user
            if window_should_close():
                terminate_window()
                sys.exit()

            # Update the drivers
            simulation.update(get_frame_time())

            # Update the visualization
            begin_drawing()
            clear_background(BLACK)
            simulation.draw()
            end_drawing()

    # Train the population
    population.run(evaluate_genomes)


def main() -> None:
    """
    Entry point into running the simulation visualization
    """
    initialize_window()
    population = load_population_from_config_file("assets/configs/config-feedforward.txt")
    run_simulation(population)
    terminate_window()


if __name__ == "__main__":
    main()
