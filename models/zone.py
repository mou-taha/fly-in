from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, List
from sys import maxsize

if TYPE_CHECKING:
    from models.connection import Connection


class ZoneType(Enum):
    NORMAL = 1
    BLOCKED = 2
    RESTRICTED = 3
    PRIORITY = 4


class ZoneCategory(Enum):
    HUB = 1
    START_HUB = 2
    END_HUB = 3


class Zone:

    def __init__(
        self,
        name: str,
        color: str,
        coordinate: tuple[int, int],
        maxDrones: int,
        type: ZoneType = ZoneType.NORMAL,
        category: ZoneCategory = ZoneCategory.HUB,
    ):
        self.name = name
        self.color = color
        self.coordinate = coordinate
        self.maxDrones = maxDrones
        self.connections: List[Connection] = []
        self.type = type
        self.category = category

    def zone_cost(self) -> float:
        """return the cost of moving to this zone
        based on zone Type
        Returns:
            float: zone cost
        """
        if self.type == ZoneType.RESTRICTED:
            return 2
        if self.type == ZoneType.NORMAL:
            return 1
        if self.type == ZoneType.PRIORITY:
            return 0.99
        else:
            return maxsize
