from models.map import Map
from models.zone import Zone, ZoneCategory
from models.path import Path
from typing import List
from helper.exceptions.path_finding_exception import PathFindingException


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
            raise PathFindingException("end zone or start zone are not defined")

        while len(unvisited) > 0:
            current: Zone = unvisited.pop()
            visited.append(current)
            unvisited.extend([connection.zone for connection
                              in current.connections
                              if connection.zone not in visited
                              and connection.zone not in unvisited])

        return end_zone in visited

    def find_paths(self) -> List[Path]:
        # if not self._check_disconnected_zones():
        #     raise PathFindingException("there is no path on the given "
        #                                "map to the end zone.")

        # start_zone: Zone = next((zone for zone in self.map.zones
        #                          if zone.type == ZoneCategory.START_HUB), None)
        # if start_zone is None:
        #     raise PathFindingException("there is no start zone on the given"
        #                                " map")

        # paths: List[tuple[Path, bool]] = (Path([start_zone]))
        # # iterate over the list of paths where path doesn't get to end
        # for path in [item[0] for item in paths
        #              if item[1] is False]:
        #     conns = path.zones[-1].connections
        # return paths
        pass

    def get_all_possible_paths(self) -> list[Path]:
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

        def dfs(current_zone: Zone, current_path: list[Zone],
                visited: set[str]):
            # Add the current zone to the path and mark it as visited
            current_path.append(current_zone)
            visited.add(current_zone.name)

            # If we reached the destination,
            # add a copy of the path to our results
            if current_zone.name == end_zone.name:
                all_paths.append(Path(list(current_path)))
            else:
                # Explore all connected zones that haven't been
                # visited in the current path
                for neighbor in current_zone.connections:
                    if neighbor.zone.name not in visited:
                        dfs(neighbor.zone, current_path, visited)

            # Backtrack: remove the current zone from path and visited set
            # so it can be explored via different routes
            current_path.pop()
            visited.remove(current_zone.name)

        # Initialize the recursive search
        dfs(start_zone, [], set())

        return all_paths
