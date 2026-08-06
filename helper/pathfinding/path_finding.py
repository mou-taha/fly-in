from models.map import Map
from models.zone import Zone, ZoneCategory
from models.path import Path
from typing import List
from helper.exceptions.path_finding_exception import PathFindingException
import heapq


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
            raise PathFindingException("end zone or start zone"
                                       " are not defined")

        while len(unvisited) > 0:
            current: Zone = unvisited.pop()
            visited.append(current)
            unvisited.extend([connection.zone for connection
                              in current.connections
                              if connection.zone not in visited
                              and connection.zone not in unvisited])

        return end_zone in visited

    def get_all_possible_paths(self) -> List[Path]:
        """
        Finds all possible simple paths between a start and end zone on a map.

        :param map_obj: The Map object containing zones and connections.
        :param start_zone_name: The name of the starting zone (e.g., 'A').
        :param end_zone_name: The name of the destination zone (e.g., 'G').
        :return: A list of paths, where each path is a list of Zone objects.
        """
        if not self._check_disconnected_zones():
            raise PathFindingException("there is no path on the given "
                                       "map to the end zone.")
        # Verify both zones exist in the map
        start_zone = next((zone for zone in self.map.zones
                           if zone.category == ZoneCategory.START_HUB), None)
        end_zone = next((zone for zone in self.map.zones
                         if zone.category == ZoneCategory.END_HUB), None)
        if start_zone is None or end_zone is None:
            return []

        all_paths: List[Path] = []

        def dfs(current_zone: Zone, current_path: list[Zone]):
            # Add the current zone to the path and mark it as visited
            # also this list contain the visited zones in the current path
            # to avoid cycles
            current_path.append(current_zone)

            # If we reached the destination,
            # add a copy of the path to our results
            if current_zone.name == end_zone.name:
                all_paths.append(Path(list(current_path)))
            else:
                # Explore all connected zones that haven't been
                # visited in the current path
                for neighbor in current_zone.connections:
                    if neighbor.zone not in current_path:
                        dfs(neighbor.zone, current_path)

            # Backtrack: remove the current zone from path and visited set
            # so it can be explored via different routes
            current_path.pop()

        # Initialize the recursive dfs function with the start zone
        dfs(start_zone, [])

        return all_paths

    def find_shortest_paths(self) -> List[Path]:
        """finding shortest path using Dijkstra"""
        if not self._check_disconnected_zones():
            raise PathFindingException("there is no path on the given "
                                       "map to the end zone.")
        start_zone: Zone = self.map.get_start_zone()
        paths: List[tuple[float, int, Path]] = [(0, 0, Path([start_zone]))]
        result: List[Path] = []
        counter: int = 0
        while paths:
            current_path_weight: float
            current_path: Path
            current_path_weight, _, current_path = paths.pop(0)
            current_zone: Zone = current_path.zones[-1]

            if current_zone.is_goal_zone():
                result.append(current_path)
                continue

            for neighbor in current_zone.connections:
                if neighbor.zone in current_path.zones:
                    continue
                new_path = Path(list.copy(current_path.zones))
                new_path.zones.append(neighbor.zone)
                heapq.heappush(paths, (neighbor.zone.zone_cost()
                               + current_path_weight, counter, new_path))
                counter += 1

        return result
