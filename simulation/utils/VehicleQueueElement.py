from .Vehicle import Vehicle

class VehicleQueueElement:
    def __init__(self, vehicle: Vehicle, progress):
        self.vehicle = vehicle
        self.progress = progress
