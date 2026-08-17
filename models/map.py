from models.connection import Connection
from typing import Dict, List

from models.drone import Drone

from .zone import Zone
from models.zone import ZoneCategory
from models.path import Path


class Map:
    """this class for represent the map"""
    def __init__(
        self,
        nbDrones: int,
        zones: set[Zone],
    ):
        self.nbDrones = nbDrones
        self.zones = zones
        self.paths: list[Path] = []
        # track connection usage per simulation turn: {Connection: used_count}
        self._connection_usage: Dict[Connection, int] = {}
        # track current simulation turn (starts at 0, incremented on reset)
        self.current_turn: int = 0
        # track when drones were added
        # to a connection: {Connection: {drone: turn_added}}
        self.connection_added_turn: Dict[Connection, Dict[Drone, int]] = {}

    def get_start_zone(self) -> Zone:
        """return the start zone of the map"""
        return next(
            zone
            for zone in self.zones
            if zone.category == ZoneCategory.START_HUB
        )

    def get_end_zone(self) -> Zone:
        """return the end zone of the map"""
        return next(
            zone
            for zone in self.zones
            if zone.category == ZoneCategory.END_HUB
        )

    def extendZoneDrones(self, zone: Zone, drones: List[Drone]) -> None:
        """Move drones to a specific zone.

        Args:
            zone: target zone
            drones: list of drones to move

        Returns:
            None"""
        if zone in self.zones:
            zone.drones.extend(drones)

    def removeZoneDrones(self, zone: Zone, drones: List[Drone]) -> None:
        """Remove drones from a specific zone

        Args:
            zone: target zone
            drones: drones to remove
        
        Returns:
            None"""
        if zone in self.zones:
            for drone in drones:
                if drone in zone.drones:
                    zone.drones.remove(drone)

    def get_connection_available(self, connection: Connection) -> int:
        """Calculate availability for a connection

        Args:
            connection: target connection

        Returns:
            positive integer represent the availability for this connection"""
        used = self._connection_usage.get(connection, 0)
        waiting = (
            len(connection.drones) if hasattr(connection, "drones") else 0
        )
        # available = capacity - already waiting on connection - already
        # reserved this turn
        return max(0, connection.maxLinkCapacity - waiting - used)

    def add_connection_usage(self, connection: Connection, count: int) -> None:
        """update connection usage

        Args:
            connection: connection to update
            count: value to add

        Returns:
            None"""
        self._connection_usage[connection] = (
            self._connection_usage.get(connection, 0) + count
        )

    def reset_connection_usage(self) -> None:
        """Clear connection usage

        Returns
            None"""
        # start a new simulation turn: clear usage counts and advance
        # the turn counter
        self._connection_usage.clear()
        self.current_turn += 1
        # clear per-connection added-turn records for completed turns
        # keep the dict entries but they will
        # be repopulated as drones are added this turn
        self.connection_added_turn.clear()

    def mark_connection_newly_added(
        self, connection: Connection, drones: List[Drone]
    ) -> None:
        """Record that these drones were added to
        `connection` on the current turn.

        Args:
            connection: target connection
            drones: drones to add

        Returns:
            None"""
        if connection not in self.connection_added_turn:
            self.connection_added_turn[connection] = {}
        for d in drones:
            self.connection_added_turn[connection][d] = self.current_turn

    def remove_connection_added_records(
        self, connection: Connection, drones: List[Drone]
    ) -> None:
        """Remove records for drones that left the connection.

        Args:
            connection: connection to update
            drones: drones to remove

        Returns:
            None"""
        if connection not in self.connection_added_turn:
            return
        for d in drones:
            self.connection_added_turn[connection].pop(d, None)
