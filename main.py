# main file for the simulation
import sys
from simulation.Simulation import Simulation

def main(argv):
    # pass argv in case of debugging etc.
    sim = Simulation(argv)
    sim.run()


if __name__ == '__main__':
    main(sys.argv[1:])
