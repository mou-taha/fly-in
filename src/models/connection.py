from ..models.zone import Zone
from typing import List


class Connection:
    """this class define a connection between two zones"""

    def __init__(self, name: str, zone: Zone, maxLinkCapacity: int):
        """Create a connection with a name, target zone, and capacity"""
        from ..models.drone import Drone

        self.zone = zone
        self.name = name
        self.maxLinkCapacity = maxLinkCapacity
        self.drones: List[Drone] = []

    def available_capacity(self) -> int:
        """return the available capacity of the connection"""
        return self.maxLinkCapacity - len(self.drones)
