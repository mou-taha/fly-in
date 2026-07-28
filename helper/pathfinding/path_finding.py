from models.map import Map
from models.zone import Zone, ZoneCategory
from typing import List


class PathFinding:
    def __init__(self, map: Map):
        self.map = map

    def check_disconnected_zones(self) -> bool:
        start_zone: Zone = [zone for zone in self.map.zones if zone.category == ZoneCategory.START_HUB][0]
        unvisited: List[Zone] = [start_zone]
        visited: list[Zone] = []

        while len(unvisited) > 0:
            current: Zone = unvisited.pop()
            visited.append(current)
            unvisited.extend([connection.zone for connection in current.connections if connection.zone not in visited and connection.zone not in unvisited])

        return len(self.map.zones) == len(visited)
