from typing import List
from models.zone import Zone, ZoneCategory, ZoneType
from models.connection import Connection


class Path:
    def __init__(self, zones: List[Zone]):
        self.zones = zones

    def get_cost(self) -> int:
        return sum([zone.zone_cost() for zone in self.zones])

    def turn(self):
        for index, target_zone in reversed(list(enumerate(self.zones))):
            if (
                target_zone.type != ZoneType.RESTRICTED
                and target_zone.category != ZoneCategory.START_HUB
            ):
                previous_zone: Zone = self.zones[index - 1]

                self.__move_drone(previous_zone, target_zone)

    def __move_drone(
        self, previous: Zone | Connection, target: Zone | Connection
    ) -> None:
        target_capacity: int = target.available_capacity()
        if target_capacity > 0 and len(previous.drones) > 0:
            drones_to_move = (
                len(previous.drones)
                if len(previous.drones) <= target_capacity
                else target_capacity
            )
            target.drones.extend(previous.drones[:drones_to_move])
            del previous.drones[:drones_to_move]
