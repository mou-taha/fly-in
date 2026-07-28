from helper.parser.dataParser import DataParser
from helper.exceptions.parsingException import ParsingException
from helper.exceptions.path_finding_exception import PathFindingExeption
from models.map import Map
from helper.pathfinding.path_finding import PathFinding


def main():
    parser: DataParser = DataParser("data.txt")
    try:
        map: Map
        map = parser.parse_network_file()
        
        path_finding: PathFinding = PathFinding(map)
        path_finding.find_paths()
        print(f"Total Drones: {map.nbDrones}")
        print(f"Total Zones Loaded: {len(map.zones)}")


        # verify the connections and metadata worked
        for zone in map.zones:
            print(f"\nInspecting {zone.name}:") 
            print(f" - Coordinate: {zone.coordinate}")
            print(f" - Type: {zone.type.name}")
            print(f" - Color: {zone.color}")
            print(f" - Max Drones: {zone.maxDrones}")
            print(
                f" - Connections: {[c.zone.name  + ' [max link capacity= ' + str(c.maxLinkCapacity) +']' for c in zone.connections]}"
            )
    except (ParsingException, PathFindingExeption) as e:
        print("error : ", e)


if __name__ == "__main__":
    main()
