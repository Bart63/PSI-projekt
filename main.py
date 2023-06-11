# main file for the simulation
import sys
from simulation import Simulation


def main(argv):
    # pass argv in case of debugging etc.
    simulation = Simulation(argv)
    simulation.run()


if __name__ == '__main__':
    main(sys.argv[1:])
