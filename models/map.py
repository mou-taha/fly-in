from .zone import Zone
from models.zone import ZoneCategory


class Map:
    def __init__(self, nbDrones: int, zones: set[Zone]):
        self.nbDrones = nbDrones
        self.zones = zones

    def get_start_zone(self) -> Zone:
        return next(zone for zone in self.zones
                    if zone.category == ZoneCategory.START_HUB)
