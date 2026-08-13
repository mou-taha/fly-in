from .zone import Zone
from models.zone import ZoneCategory
from models.path import Path


class Map:
    def __init__(self, nbDrones: int, zones: set[Zone], ):
        self.nbDrones = nbDrones
        self.zones = zones
        self.paths: list[Path] = []
        # track connection usage per simulation turn: {Connection: used_count}
        self._connection_usage: dict = {}
        # track current simulation turn (starts at 0, incremented on reset)
        self.current_turn: int = 0
        # track when drones were added to a connection: {Connection: {drone: turn_added}}
        self._connection_added_turn: dict = {}

    def get_start_zone(self) -> Zone:
        return next(zone for zone in self.zones
                    if zone.category == ZoneCategory.START_HUB)

    def get_end_zone(self) -> Zone:
        return next(zone for zone in self.zones
                    if zone.category == ZoneCategory.END_HUB)

    def extendZoneDrones(self, zone: Zone, drones: list):
        if zone in self.zones:
            zone.drones.extend(drones)

    def removeZoneDrones(self, zone: Zone, drones: list):
        if zone in self.zones:
            for drone in drones:
                if drone in zone.drones:
                    zone.drones.remove(drone)

    # Connection usage helpers (per-turn)
    def get_connection_available(self, connection) -> int:
        used = self._connection_usage.get(connection, 0)
        waiting = len(connection.drones) if hasattr(connection, 'drones') else 0
        # available = capacity - already waiting on link - already reserved this turn
        return max(0, connection.maxLinkCapacity - waiting - used)

    def add_connection_usage(self, connection, count: int) -> None:
        self._connection_usage[connection] = self._connection_usage.get(connection, 0) + count

    def reset_connection_usage(self) -> None:
        # start a new simulation turn: clear usage counts and advance the turn counter
        self._connection_usage.clear()
        self.current_turn += 1
        # clear per-connection added-turn records for completed turns
        # keep the dict entries but they will be repopulated as drones are added this turn
        self._connection_added_turn.clear()

    def mark_connection_newly_added(self, connection, drones: list) -> None:
        """Record that these drones were added to `connection` on the current turn."""
        if connection not in self._connection_added_turn:
            self._connection_added_turn[connection] = {}
        for d in drones:
            self._connection_added_turn[connection][d] = self.current_turn

    def remove_connection_added_records(self, connection, drones: list) -> None:
        """Remove records for drones that left the connection."""
        if connection not in self._connection_added_turn:
            return
        for d in drones:
            self._connection_added_turn[connection].pop(d, None)
