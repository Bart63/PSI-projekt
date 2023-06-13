# example implementation of driver
from simulation.api import API
from .Driver import Driver


class DummyDriver(Driver):
    def __init__(self):
        super().__init__()
