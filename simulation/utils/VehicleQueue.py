from typing import List
from .VehicleQueueElement import VehicleQueueElement
from .Vehicle import Vehicle
import config as cfg

class VehicleQueue:
    def __init__(self, road_length, start_pos, end_pos, is_green_callback, padding=10):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.queue:List[VehicleQueueElement] = []
        self.road_length = road_length
        self.progress_step = cfg.VEHICLE_PROGRESS_STEP / self.road_length
        self.padding = padding
        self.is_green_callback = is_green_callback
    
    def is_busy(self):
        return self.queue and self.queue[-1].progress == 0

    def enqueue(self, vehicle: Vehicle):
        vehicle.x, vehicle.y = self.start_pos
        self.queue.append(VehicleQueueElement(vehicle, progress=0))
        vehicle.on_road_start()

    def move_closer(self) -> List[VehicleQueueElement]:
        last_progress = None
        finished_vqes = []
        for vqe in self.queue:
            vqe.vehicle.on_tick()
            if vqe.progress == 1 and not self.is_green_callback():
                last_progress = vqe.progress
                continue
            if last_progress and vqe.progress + (self.padding/self.road_length) + self.progress_step >= last_progress:
                last_progress = vqe.progress
                continue
            last_progress = vqe.progress
            vqe.progress = min(vqe.progress + self.progress_step, 1)

            new_x = last_progress*(self.end_pos[0] - self.start_pos[0]) + self.start_pos[0]
            new_y = last_progress*(self.end_pos[1] - self.start_pos[1]) + self.start_pos[1]
            vqe.vehicle.drive(new_x, new_y)

            if vqe.progress == 1 and self.is_green_callback():
                vqe.vehicle.on_road_end()
                finished_vqes.append(vqe)
        return finished_vqes
