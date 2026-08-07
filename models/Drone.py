from models.zone import Zone
from models.connection import Connection


class Drone:
    def __init__(self, id: int, assigned_path: list[Zone],
                 current_place: Zone | Connection):
        self.id = id
        self.assigned_path = assigned_path
        self.current_place = current_place
