import yaml
import config as cfg
import drivers as drv


def set_yaml_config(file_path: str, driver_name: str, test_no: int):
    with open(file_path, 'r') as stream:
        configuration = yaml.safe_load(stream)
    driver_tests = configuration['driver_tests'].get(driver_name)
    test_type = 'unique' if driver_tests is not None else 'default'
    driver_tests = driver_tests if driver_tests is not None else configuration['default_tests']
    test_config = driver_tests.get(f'Test_{test_no}')
    cfg.MAIN_VEHICLE_DRIVER = getattr(drv, driver_name)()
    print(f'Running {test_type} Test {test_no} for {driver_name}')
    for parameter_name, value in test_config.items():
        setattr(cfg, parameter_name, value)
        print(f'{parameter_name} = {value}')
