from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, List


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

    def __init__(self, name: str, color: str, coordinate: tuple[int, int],
                 maxDrones: int,
                 zoneType: ZoneType = ZoneType.NORMAL,
                 category: ZoneCategory = ZoneCategory.HUB):
        self.name = name
        self.color = color
        self.coordinate = coordinate
        self.maxDrones = maxDrones
        self.connections: List[Connection] = []
        self.zoneType = zoneType
        self.category = category
