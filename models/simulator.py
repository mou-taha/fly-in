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

        turns: str = ""
        while len(end_zone.drones) < self.map.nbDrones:
            # reset per-turn connection usage so we start counting capacity fresh each simulation turn
            self.map.reset_connection_usage()
            turns: str = ""
            for path in self.map.paths:
                turns += path.turn()
            if turns != "":
                print(turns)
