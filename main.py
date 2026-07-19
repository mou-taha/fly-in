from helper.parser.dataParser import DataParser
from helper.exceptions.parsingException import ParsingException
from models.space import Space


def main():
    parser: DataParser = DataParser("data.txt")
    my_space: Space
    try:
        my_space = parser.parse_network_file()
    except ParsingException as e:
        print(e)
        return

    print(f"Total Drones: {my_space.nbDrones}")
    print(f"Total Zones Loaded: {len(my_space.zones)}")

    # verify the connections and metadata worked
    for zone in my_space.zones:
        print(f"\nInspecting {zone.name}:")
        print(f" - Coordinate: {zone.coordinate}")
        print(f" - Type: {zone.zoneType.name}")
        print(f" - Color: {zone.color}")
        print(f" - Max Drones: {zone.maxDrones}")
        print(f" - Connections: {[c.zone.name  + ' [max link capacity= ' + str(c.maxLinkCapacity) +']' for c in zone.connections]}")


if __name__ == "__main__":
    main()
