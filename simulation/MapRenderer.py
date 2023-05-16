from simulation.Map import Map


class MapRenderer:
    def __init__(self, map_: Map, base_image=None):
        self.base_image = base_image
        self.map_ = map_

    # render given layers of map
    def render_base(self):
        pass

    def render_roads(self):
        pass

    def render_vehicles(self):
        pass
