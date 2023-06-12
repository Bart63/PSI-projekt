from typing import List
from .VehicleQueueElement import VehicleQueueElement
from .Vehicle import Vehicle


PROGRESS_STEP = 1

class VehicleQueue:
    def __init__(self, road_length, start_pos, end_pos, is_green_callback, padding=0.2):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.queue:List[VehicleQueueElement] = []
        self.road_length = road_length
        self.progress_step = PROGRESS_STEP / self.road_length
        self.padding = padding
        self.is_green_callback = is_green_callback

    def enqueue(self, vehicle: Vehicle):
        vehicle.x, vehicle.y = self.start_pos
        self.queue.append(VehicleQueueElement(vehicle, progress=0))

    def move_closer(self):
        last_progress = None
        finished_vehicles = []
        for vqe in self.queue:
            if vqe.progress >= 1 and not self.is_green_callback():
                break
            if last_progress and vqe.progress + self.padding + self.progress_step >= last_progress:
                continue
            vqe.progress += self.progress_step
            last_progress = vqe.progress

            vqe.vehicle.x, vqe.vehicle.y = last_progress*(self.end_pos[0] - self.start_pos[0]) + self.start_pos[0], last_progress*(self.end_pos[1] - self.start_pos[1]) + self.start_pos[1] 

            if vqe.progress >= 1 and self.is_green_callback():
                finished_vehicles.append(vqe.vehicle)
                self.queue.remove(vqe)
        return finished_vehicles
