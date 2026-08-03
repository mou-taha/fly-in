from typing import List
from models.zone import Zone, ZoneCategory, ZoneType


class Path:
    def __init__(self, zones: List[Zone]):
        self.zones = zones

    def get_cost(self) -> int:
        cost = 0
        for zone in self.zones:
            if zone.category == ZoneCategory.START_HUB:
                continue
            if zone.type == ZoneType.NORMAL:
                cost = cost + 1
            elif zone.type == ZoneType.RESTRICTED:
                cost = cost + 2
            elif zone.type == ZoneType.BLOCKED:
                cost = cost + 1
            elif zone.type == ZoneType.PRIORITY:
                cost = cost + 0.99
        return cost
