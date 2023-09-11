import yaml
import config as cfg
import drivers as drv


def set_yaml_config(file_path: str, driver_name: str, test_no: int, test_type='default'):
    with open(file_path, 'r') as stream:
        configuration = yaml.safe_load(stream)
    driver_tests = configuration['driver_tests'].get(driver_name)
    driver_tests = driver_tests if test_type == 'unique' else configuration['default_tests']
    test_config = driver_tests.get(f'Test_{test_no}')
    test_config = {} if test_config==None else test_config
    cfg.MAIN_VEHICLE_DRIVER = getattr(drv, driver_name)()
    print(f'\nRunning {test_type} Test {test_no} for {driver_name}')
    for parameter_name, value in test_config.items():
        setattr(cfg, parameter_name, value)
        print(f'{parameter_name} = {value}')


def get_test_no(file_path: str, driver_name: str):
    with open(file_path, 'r') as stream:
        configuration = yaml.safe_load(stream)
    driver_tests = configuration['driver_tests'].get(driver_name)
    default_tests = configuration['default_tests']
    return len(default_tests) if default_tests else 0, len(driver_tests) if driver_tests else 0
