from typing import List
from models.zone import Zone, ZoneCategory, ZoneType
from models.connection import Connection


class Path:
    def __init__(self, zones: List[Zone]) -> None:
        self.zones = zones

    def get_cost(self) -> float:
        return sum([zone.zone_cost() for zone in self.zones])

    def turn(self) -> str:
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
        return turns

    # TODO fix when deleting drone from one path it deleted from other path
    def __move_drone(
        self, previous: Zone | Connection, target: Zone | Connection
    ) -> str:
        target_capacity: int = target.available_capacity()
        if target_capacity > 0 and len(previous.drones) > 0:
            nb_drones_to_move: int = (
                len(previous.drones)
                if len(previous.drones) <= target_capacity
                else target_capacity
            )

            # check if connection support the number of drones
            # that will be travers it to target wone
            if isinstance(previous, Zone):
                traversal: Connection = next(
                    cn
                    for cn in previous.connections
                    if cn.zone.name == target.name
                )
                if nb_drones_to_move > traversal.maxLinkCapacity:
                    nb_drones_to_move = traversal.maxLinkCapacity

            drone_to_move = previous.drones[:nb_drones_to_move]
            msg: str = ""
            for drone in drone_to_move:
                drone.current_place = target
                msg += f"D{drone.id}-{drone.current_place.name} "
            target.drones.extend(drone_to_move)
            for d in drone_to_move:
                previous.drones.remove(d)
            return msg
        return ""
