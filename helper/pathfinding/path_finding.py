from models.map import Map
from models.zone import Zone, ZoneCategory
from typing import List
from helper.exceptions.path_finding_exception import PathFindingExeption

class PathFinding:
    def __init__(self, map: Map):
        self.map = map

    def _check_disconnected_zones(self) -> bool:
        start_zone: Zone = [zone for zone in self.map.zones
                            if zone.category == ZoneCategory.START_HUB][0]
        end_zone: Zone = [zone for zone in self.map.zones
                          if zone.category == ZoneCategory.END_HUB][0]
        unvisited: List[Zone] = [start_zone]
        visited: list[Zone] = []
        if not end_zone or not start_zone:
            raise PathFindingExeption("end zone or start zone are not defined")

        while len(unvisited) > 0:
            current: Zone = unvisited.pop()
            visited.append(current)
            unvisited.extend([connection.zone for connection in current.connections if connection.zone not in visited and connection.zone not in unvisited])

        return end_zone in visited

    def find_paths(self) -> List[Zone]:
        if not self._check_disconnected_zones():
            raise PathFindingExeption("there is no path on the given "
                                      "map to the end zone.")
        