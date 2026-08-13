from models.zone import Zone
from typing import List


class Connection:

    def __init__(self, name: str, zone: Zone, maxLinkCapacity: int):
        from models.drone import Drone

        self.zone = zone
        self.name = name
        self.maxLinkCapacity = maxLinkCapacity
        self.drones: List[Drone] = []

    def available_capacity(self) -> int:
        """return the available capacity of the zone"""
        return self.maxLinkCapacity - len(self.drones)
