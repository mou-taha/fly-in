from typing import List
from models.zone import Zone, ZoneCategory, ZoneType
from models.connection import Connection


class Path:
    def __init__(self, zones: List[Zone]):
        self.zones = zones

    def get_cost(self) -> int:
        return sum([zone.zone_cost() for zone in self.zones])

    def turn(self):
        turns: str = ""
        for index, target_zone in reversed(list(enumerate(self.zones))):
            if (
                target_zone.type != ZoneType.RESTRICTED
                and target_zone.category != ZoneCategory.START_HUB
            ):
                previous_zone: Zone = self.zones[index - 1]
            res: str = self.__move_drone(previous_zone, target_zone)
            if res is not None:
                turns += res
        print(turns)

    def __move_drone(
        self, previous: Zone | Connection, target: Zone | Connection
    ) -> str:
        target_capacity: int = target.available_capacity()
        if target_capacity > 0 and len(previous.drones) > 0:
            drones_to_move = (
                len(previous.drones)
                if len(previous.drones) <= target_capacity
                else target_capacity
            )
            drone_to_move = previous.drones[:drones_to_move]
            msg: str = ""
            for drone in drone_to_move:
                drone.current_place = target
                msg += f"D{drone.id}-{drone.current_place.name} "
            target.drones.extend(drone_to_move)
            del previous.drones[:drones_to_move]
            return msg
