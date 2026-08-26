from ..models.path import Path
from ..models.zone import Zone
from ..models.connection import Connection


class Drone:
    """this class is a representation of a drone inside a map"""

    def __init__(
        self, id: int, assigned_path: Path, current_place: Zone | Connection
    ):
        """Create a drone with its assigned path and current location.

        Args:
            id (int): id of the drone
            assigned_path (Path): assigned path.
            current_place (Zone | Connection): actual zone during simulation.
        """
        self.id = id
        self.assigned_path = assigned_path
        self.current_place = current_place
