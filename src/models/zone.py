from enum import Enum
from typing import TYPE_CHECKING, List
from sys import maxsize

if TYPE_CHECKING:
    from ..models.connection import Connection


class ZoneType(Enum):
    """Types of zones used by the simulation."""

    NORMAL = 1
    BLOCKED = 2
    RESTRICTED = 3
    PRIORITY = 4


class ZoneCategory(Enum):
    """Categories used to identify map hubs."""

    HUB = 1
    START_HUB = 2
    END_HUB = 3


class Zone:
    """A map node with coordinates, capacity, and connections"""

    def __init__(
        self,
        name: str,
        color: str,
        coordinate: tuple[int, int],
        maxDrones: int,
        type: ZoneType = ZoneType.NORMAL,
        category: ZoneCategory = ZoneCategory.HUB,
    ):
        """Create a zone with its name, position, and rules."""
        from ..models.drone import Drone

        self.name = name
        self.color = color
        self.coordinate = coordinate
        self.maxDrones = maxDrones
        self.connections: List[Connection] = []
        self.type = type
        self.category = category
        self.drones: List[Drone] = []

    def zone_cost(self) -> float:
        """return the cost of moving to this zone
        based on zone Type
        Returns:
            float: zone cost
        """
        if self.category == ZoneCategory.START_HUB:
            return 0
        elif self.type == ZoneType.RESTRICTED:
            return 2
        elif self.type == ZoneType.NORMAL:
            return 1
        elif self.type == ZoneType.PRIORITY:
            return 0.99
        else:
            return maxsize

    def is_goal_zone(self) -> bool:
        """Return whether this zone is the end hub.

        Returns:
            bool: true if zone is goal zone, otherwise false.
        """
        return self.category == ZoneCategory.END_HUB

    def available_capacity(self) -> int:
        """return the available capacity of the zone"""
        return self.maxDrones - len(self.drones)
