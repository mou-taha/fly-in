from typing import List
from ..models.zone import Zone, ZoneCategory, ZoneType
from ..models.connection import Connection
from ..helper.terminal.terminal import color_text


class Path:
    """represent a single path from start zone to the goal inside map."""

    def __init__(self, zones: List[Zone]) -> None:
        """create a path from a list of zones."""
        from ..models.map import Map
        from ..models.drone import Drone

        self.zones = zones
        self.map: Map = Map(0, set())
        # per-path drone storage: map each Zone
        # in this path to its own list of drones
        self.zone_drones: dict[Zone, List[Drone]] = {
            zone: [] for zone in zones
        }

    def get_cost(self) -> int:
        """Return the total cost of the path.

        Returns:
            int: cost.
        """
        return int(sum([zone.zone_cost() for zone in self.zones]))

    def turn(self) -> str:
        """move drones from connection or zone to a another connection or zone.

        Returns:
            str: return the turns that has been executed
        """
        turns: str = ""
        for index, target_zone in reversed(list(enumerate(self.zones))):
            # process all zones except the start hub; restricted zones are
            # handled by moving drones onto the connection and flushing later
            if target_zone.category != ZoneCategory.START_HUB:
                previous_zone: Zone = self.zones[index - 1]
                # if there is a connection between previous_zone
                # and target_zone, first try to move any drones waiting
                # on that connection into the target zone
                traversal_conn = next(
                    (
                        cn
                        for cn in previous_zone.connections
                        if cn.zone.name == target_zone.name
                    ),
                    None,
                )
                if traversal_conn is not None:
                    turns += self._move_drones_in_connection(
                        traversal_conn, target_zone
                    )
                turns += self.__move_drone(previous_zone, target_zone)
        return turns

    def _move_drones_in_connection(
        self, connection: Connection, target_zone: Zone
    ) -> str:
        """Try to move drones waiting on a connection into the target zone
        when capacity allows.

        Args:
            connection (Connection): connection to check.
            target_zone (Zone): target zone.

        Returns:
            str: turn
        """
        if not connection.drones:
            return ""

        # determine target capacity

        target_capacity = target_zone.available_capacity()

        if target_capacity <= 0:
            return ""

        # only move drones that were NOT added to this
        # connection in the current turn
        added_turns = self.map.connection_added_turn.get(connection, {})
        eligible = [
            d
            for d in connection.drones
            if added_turns.get(d, -1) < self.map.current_turn
        ]

        if not eligible:
            return ""

        nb_to_move = min(len(eligible), target_capacity)
        moving = eligible[:nb_to_move]

        for d in moving:
            d.current_place = target_zone

        # add to this path's per-zone list
        self.zone_drones.setdefault(target_zone, []).extend(moving)
        turns: str = ""
        # remove from connection and update map canonical lists
        for d in moving:
            connection.drones.remove(d)
        # remove added-turn records for moved drones
        self.map.remove_connection_added_records(connection, moving)
        self.map.extendZoneDrones(target_zone, moving)
        for d in moving:
            turns += f"D{d.id}-{d.current_place.name} "
        return turns

    def __move_drone(self, previous: Zone, target: Zone) -> str:
        """move drones from a zone to another zone if capacity allow

        Args:
            previous (Zone): zone that hold drones
            target (Zone): zone that will hold new drones

        Returns:
            str: turn
        """
        target_capacity = target.available_capacity()
        prev_list = self.zone_drones.get(previous, [])

        # move drones if only capacity allow and if there is drones
        # on previous zone
        if target_capacity > 0 and len(prev_list) > 0:

            # check if connection supports the number of drones
            # that will traverse to target zone
            traversal: Connection = next(
                cn
                for cn in previous.connections
                if cn.zone.name == target.name
            )
            # enforce shared connection capacity across paths
            # using map connection usage
            conn_available = self.map.get_connection_available(traversal)
            nb_drones_to_move = min(
                len(prev_list), target_capacity, conn_available
            )
            drone_to_move = prev_list[:nb_drones_to_move]
            msg: str = ""

            # reserve connection capacity immediately so subsequent
            # paths in this turn see the reduced available capacity
            traversal_conn = next(
                cn
                for cn in previous.connections
                if cn.zone.name == target.name
            )
            self.map.add_connection_usage(traversal_conn, len(drone_to_move))

            # If the target is a restricted zone, drones must move in two turns
            # so it must move to the connection after to the target zone
            if target.type == ZoneType.RESTRICTED:
                # place drones on the connection (they are waiting to enter)
                traversal_conn.drones.extend(drone_to_move)
                # mark these drones as added on the current turn so they won't
                # be flushed immediately
                self.map.mark_connection_newly_added(
                    traversal_conn, drone_to_move
                )
                for drone in drone_to_move:
                    drone.current_place = target
                    msg += f"D{drone.id}-{traversal_conn.name} "
            # if the target is a normal zone the move to it cost one turn
            else:
                # update global map zone lists and per-path tracking
                self.map.extendZoneDrones(target, drone_to_move)

                # add to target per-path list and remove
                # from previous per-path list
                self.zone_drones.setdefault(target, []).extend(drone_to_move)
                for drone in drone_to_move:
                    drone.current_place = target
                    colored_zone = color_text(
                        drone.current_place.name, drone.current_place.color
                    )
                    msg += f"D{drone.id}-" + "" + f"{colored_zone} "

            for d in drone_to_move:
                self.zone_drones[previous].remove(d)
            self.map.removeZoneDrones(previous, drone_to_move)
            return msg
        return ""
