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


class Zone:

    def __init__(self, name: str, color: str, coordinate: tuple[int, int],
                 maxDrones: int, connection: List[Connection],
                 zoneType: ZoneType = ZoneType.NORMAL):
        self.name = name
        self.color = color
        self.coordinate = coordinate
        self.maxDrones = maxDrones
        self.connection = connection
        self.zoneType = zoneType
