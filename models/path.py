from typing import List
from models.zone import Zone


class Path:
    def __init__(self, zones: List[Zone]):
        self.zones = zones

    def get_cost(self) -> int:
        return sum([zone.zone_cost() for zone in self.zones])
