from models.connection import Connection
from models.path import Path
from models.zone import Zone


class Drone:

    def __init__(
        self, id: int, assigned_path: Path, current_place: Zone | Connection
    ):
        self.id = id
        self.assigned_path = assigned_path
        self.current_place = current_place
