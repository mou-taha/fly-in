from helper.parser.dataParser import DataParser
from helper.exceptions.parsingException import ParsingException
from helper.exceptions.path_finding_exception import PathFindingException
from models.map import Map
from models.path import Path
from helper.pathfinding.path_finding import PathFinding


def main():
    parser: DataParser = DataParser("data.txt")
    try:
        map: Map
        map = parser.parse_network_file()

        path_finding: PathFinding = PathFinding(map)
        print(f"Total Drones: {map.nbDrones}")
        print(f"Total Zones Loaded: {len(map.zones)}")

        paths: list[Path] = path_finding.get_all_possible_paths()
        print(f"Total Paths: {len(paths)}")

        # 5. Print the results
        for i, path in enumerate(paths, 1):
            path_names = [zone.name for zone in path.zones]
            print(f"Path {i}: {' -> '.join(path_names)}")
            print(f"Path cost: {path.get_cost()}")

        # verify the connections and metadata worked
        # for zone in map.zones:
        #     print(f"\nInspecting {zone.name}:") 
        #     print(f" - Coordinate: {zone.coordinate}")
        #     print(f" - Type: {zone.type.name}")
        #     print(f" - Color: {zone.color}")
        #     print(f" - Max Drones: {zone.maxDrones}")
        #     print(
        #         f" - Connections: {[c.zone.name  + ' [max link capacity= ' + str(c.maxLinkCapacity) +']' for c in zone.connections]}"
        #     )
    except (ParsingException, PathFindingException) as e:
        print(e)


if __name__ == "__main__":
    main()
