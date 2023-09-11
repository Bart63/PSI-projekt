# main file for the simulation
import sys
from simulation import Simulation
from simulation.utils.YamlConfigParser import get_test_no


def main(argv):
    driver_to_test = ""
    test_no = -1
    if len(argv) == 2:
        driver_to_test = argv[0]
        test_no = int(argv[1])
    if test_no == -1 and driver_to_test != '':
        tests = get_test_no('configurations.yaml', driver_to_test)
        print('Default TESTS')
        for test in range(1, tests[0] + 1):
            simulation = Simulation(driver_to_test, test, 'default')
            result = simulation.run()

            for key, value in result.items():
                print(f'{key}:\t{value}')
        if tests[1] > 0:
            print('\nUnique TESTS')
        for test in range(1, tests[1] + 1):
            simulation = Simulation(driver_to_test, test, 'unique')
            result = simulation.run()

            for key, value in result.items():
                print(f'{key}:\t{value}')
    else:
        simulation = Simulation(driver_to_test, test_no, 'unique')
        result = simulation.run()
        for key, value in result.items():
            print(f'{key}:\t{value}')


if __name__ == '__main__':
    main(sys.argv[1:])
