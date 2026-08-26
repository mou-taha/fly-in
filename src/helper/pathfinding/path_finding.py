from ...models.map import Map
from ...models.zone import Zone, ZoneCategory, ZoneType
from ...models.path import Path
from typing import List
from ...helper.exceptions import PathFindingException


class PathFinding:
    """Path-finding utilities for the map."""

    def __init__(self, map: Map):
        """Create a parser for a map file."""
        self.map = map

    def _check_disconnected_zones(self) -> bool:
        """check if the map has no path to the goal.

        Raises:
            PathFindingException: if there is no start or end zone.

        Returns:
            bool: True if there is at least one path to the end zone,
                False if there is no path to the goal zone
        """
        start_zone: Zone = [
            zone
            for zone in self.map.zones
            if zone.category == ZoneCategory.START_HUB
        ][0]
        end_zone: Zone = [
            zone
            for zone in self.map.zones
            if zone.category == ZoneCategory.END_HUB
        ][0]
        unvisited: List[Zone] = [start_zone]
        visited: set[Zone] = set()
        if not end_zone or not start_zone:
            raise PathFindingException(
                "end zone or start zone" " are not defined"
            )

        while len(unvisited) > 0:
            current: Zone = unvisited.pop()
            visited.add(current)
            if end_zone == current:
                return True
            unvisited.extend(
                [
                    connection.zone
                    for connection in current.connections
                    if connection.zone not in visited
                    and connection.zone not in unvisited
                ]
            )

        return False

    def get_all_possible_paths(self) -> List[Path]:
        """Finds all possible simple paths between a start
        and end zone on a map.

        Raises:
            PathFindingException: _description_

        Returns:
            List[Path]:A list of paths, where each path
            is a list of Zone objects.
        """
        if not self._check_disconnected_zones():
            raise PathFindingException(
                "there is no path on the given " "map to the end zone."
            )
        # Verify both zones exist in the map
        start_zone = next(
            (
                zone
                for zone in self.map.zones
                if zone.category == ZoneCategory.START_HUB
            ),
            None,
        )
        end_zone = next(
            (
                zone
                for zone in self.map.zones
                if zone.category == ZoneCategory.END_HUB
            ),
            None,
        )
        if start_zone is None or end_zone is None:
            return []

        all_paths: List[Path] = []

        def dfs(current_zone: Zone, current_path: list[Zone]) -> None:
            """dfs algo for path finding.

            Args:
                current_zone (Zone): current zone.
                current_path (list[Zone]): actual path.
            """
            # Add the current zone to the path and mark it as visited
            # also this list contain the visited zones in the current path
            # to avoid cycles
            current_path.append(current_zone)

            # if the zone is blocked we will not continue the path
            if current_zone.type == ZoneType.BLOCKED:
                current_path.pop()
                return

            # If we reached the destination,
            # add a copy of the path to our results
            if current_zone.name == end_zone.name:
                path = Path(list(current_path))
                path.map = self.map
                all_paths.append(path)
            else:
                # Explore all connected zones that haven't been
                # visited in the current path
                for neighbor in current_zone.connections:
                    if neighbor.zone not in current_path:
                        dfs(neighbor.zone, current_path)

            # Backtrack: remove the current zone from path
            # so it can be explored via different routes
            current_path.pop()

        # Initialize the recursive dfs function with the start zone
        dfs(start_zone, [])
        all_paths = sorted(all_paths, key=lambda path: path.get_cost())
        return all_paths
