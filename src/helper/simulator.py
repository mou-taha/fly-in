from ..models.map import Map
from ..models.zone import Zone
from .exceptions.simulation_exception import SimulationException
from typing import List


class Simulator:
    def __init__(self, map: Map):
        self.map = map

    def run(self) -> List[str]:
        if len(self.map.paths) == 0:
            raise SimulationException("no path to follow")
        end_zone: Zone = self.map.get_end_zone()

        turns: List[str] = []
        while len(end_zone.drones) < self.map.nbDrones:
            self.map.reset_connection_usage()
            turn = ""
            for path in self.map.paths:
                turn += path.turn()
            if turn != "":
                turns.append(turn)
        return turns
