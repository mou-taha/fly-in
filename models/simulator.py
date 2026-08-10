from models.map import Map
from models.zone import Zone
from helper.exceptions.simulation_exception import SimulationException


class Simulator:
    def __init__(self, map: Map):
        self.map = map

    def run(self):
        if len(self.map.paths) == 0:
            raise SimulationException("no path to follow")
        end_zone: Zone = self.map.get_end_zone()

        def turn() -> None:
            for path in self.map.paths:
                path.turn()

        while len(end_zone.drones) < self.map.nbDrones:
            turn()
