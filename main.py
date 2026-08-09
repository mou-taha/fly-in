from helper.parser.dataParser import DataParser
from helper.exceptions.parsingException import ParsingException
from helper.exceptions.path_finding_exception import PathFindingException
from helper.exceptions.simulation_exception import SimulationException
from models.map import Map
from models.path import Path
from helper.pathfinding.path_finding import PathFinding
from models.simulator import Simulator


def main():
    parser: DataParser = DataParser("data.txt")
    try:
        map: Map
        map = parser.parse_network_file()

        path_finding: PathFinding = PathFinding(map)
        print(f"Total Drones: {map.nbDrones}")
        print(f"Total Zones Loaded: {len(map.zones)}")

        print("\n\n\n\n\nFinding all possible paths:")
        paths: list[Path] = path_finding.get_all_possible_paths()
        print(f"Total Paths: {len(paths)}")
        # for i, path in enumerate(paths, 1):
        #     path_names = [zone.name for zone in path.zones]
        #     print(f"Path {i}: {' -> '.join(path_names)}")
        #     print(f"Path cost: {path.get_cost()}")
        map.paths = paths
        simulator: Simulator = Simulator(map)
        simulator.run()
    except (ParsingException, PathFindingException, SimulationException) as e:
        print(e)


if __name__ == "__main__":
    main()
