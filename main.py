from helper.parser.dataParser import DataParser
from helper.exceptions.parsingException import ParsingException
from helper.exceptions.path_finding_exception import PathFindingException
from helper.exceptions.simulation_exception import SimulationException
from models.map import Map
from models.path import Path
from helper.pathfinding.path_finding import PathFinding
from models.simulator import Simulator
from models.drone import Drone


def main():
    parser: DataParser = DataParser("data.txt")
    try:
        map: Map
        map = parser.parse_network_file()

        path_finding: PathFinding = PathFinding(map)
        # print(f"Total Drones: {map.nbDrones}")
        # print(f"Total Zones Loaded: {len(map.zones)}")

        paths: list[Path] = path_finding.get_all_possible_paths()
        print(f"Total Paths: {len(paths)}")
        # for i, path in enumerate(paths, 1):
        #     path_names = [zone.name for zone in path.zones]
        #     print(f"Path {i}: {' -> '.join(path_names)}")
        #     print(f"Path cost: {path.get_cost()}")

        # take just the first path or first two paths
        map.paths = paths[:2]
        # split the drones on the different paths
        if len(map.paths) > 1:
            amount_1 = map.nbDrones // 2
            map.paths[0].zones[0].drones = [
                Drone(index + 1, map.paths[0], map.paths[0].zones[0])
                for index in range(amount_1)
            ]
            map.paths[1].zones[0].drones = [
                Drone(index + 1, map.paths[1], map.paths[1].zones[0])
                for index in range(amount_1, map.nbDrones)
            ]
        else:
            map.paths[0].zones[0].drones = [
                Drone(index + 1, map.paths[0], map.paths[0].zones[0])
                for index in range(map.nbDrones)
            ]
        simulator: Simulator = Simulator(map)
        simulator.run()
    except (ParsingException, PathFindingException, SimulationException) as e:
        print(e)


if __name__ == "__main__":
    main()
