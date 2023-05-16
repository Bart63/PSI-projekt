from simulation.utils.MapUtils import Vehicle, Crossroad


class Map:
    def __init__(self):
        self.vehicles = []
        self.crossroads = []

    # builder methods e.g.
    def with_crossroads(self, number: int):
        # generate crossroads with given number matching builder pattern
        return self

    def default(self):
        # default map generation
        return self.with_crossroads(10)

    def generate(self):
        pass
