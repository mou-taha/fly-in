from models.zone import Zone, ZoneType
from models.connection import Connection
from models.space import Space
from typing import Any
from ..exceptions.parsingException import ParsingException


class DataParser:
    def __init__(self, filePath: str) -> None:
        self.filePath = filePath

    def parse_network_file(self) -> Space:
        nb_drones = -1
        # dictionary to quickly look up zones by name
        zones_dict: dict[str, Zone] = {}
        # store connection lines to process after  all zones are created
        connections_data: list[str] = []
        keyCounter: int = 0

        with open(self.filePath, 'r') as file:
            for line in file:
                line = line.strip()

                # skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    continue

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key == "nb_drones":
                    keyCounter += 1
                    try:
                        nb_drones = int(value)
                    except ValueError:
                        raise ParsingException("""nb_drones must be a positif integer.""")
                elif key in ("hub", "start_hub", "end_hub"):
                    keyCounter += 1
                    # 1. Extract metadata
                    base_text, meta_dict = self.extract_metadata(value)

                    # 2. Parse base text: "name x y"
                    parts = base_text.split()
                    name = parts[0]
                    x = int(parts[1])
                    y = int(parts[2])

                    # 3. Apply defaults & metadata
                    # Default values based on your rules
                    color: str = meta_dict.get("color", "none")
                    max_drones = int(meta_dict.get("max_drones", 1))

                    # Parse the ZoneType Enum securely
                    zone_type_str = meta_dict.get("zone", "normal").upper()
                    try:
                        zone_type = ZoneType[zone_type_str]
                    except KeyError:
                        zone_type = ZoneType.NORMAL

                    # 4. Create Zone and store it in our dictionary
                    zone = Zone(
                        name=name,
                        color=color,
                        coordinate=(x, y),
                        maxDrones=max_drones,
                        zoneType=zone_type
                    )
                    zones_dict[name] = zone

                elif key == "connection":
                    keyCounter += 1
                    # save connections to process after all zones are created
                    connections_data.append(value)

                if keyCounter >= 1 and nb_drones == -1:
                    raise ParsingException(""" The first line must define
                                           the number of drones using
                                           nb_drones: <positive_integer>.""")

        # 5. process Connections now that all Zones exist
        for conn_str in connections_data:
            base_text, meta_dict = self.extract_metadata(conn_str)

            # connections are formatted as "zoneA-zoneB"
            if "-" in base_text:
                nameA, nameB = base_text.split("-", 1)

                # retrieve the actual Zone objects we created earlier
                zoneA: Zone | None = zones_dict.get(nameA)
                zoneB: Zone | None = zones_dict.get(nameB)

                if zoneA and zoneB:
                    capacity = int(meta_dict.get("max_link_capacity", 1))

                    # it's bidirectional, so we add
                    # a Connection object to BOTH zones
                    zoneA.connections.append(Connection(
                        zone=zoneB,
                        maxLinkCapacity=capacity))
                    zoneB.connections.append(Connection(
                        zone=zoneA,
                        maxLinkCapacity=capacity))

        # 6. Create the Space object containing all our zones
        space = Space(nbDrones=nb_drones, zones=set(zones_dict.values()))

        return space

    def extract_metadata(self, text: str) -> tuple[str, dict[str, Any]]:
        """
        Separates the base text from the metadata brackets.
        Returns: (base_text, metadata_dict)
        """
        if "[" in text and "]" in text:
            base, meta_raw = text.split("[", 1)
            base = base.strip()
            meta_raw = meta_raw.replace("]", "").strip()

            # Convert "zone=restricted color=red" into
            # {'zone': 'restricted', 'color': 'red'}
            meta_dict: dict[str, Any] = {}
            for item in meta_raw.split():
                if "=" in item:
                    key, val = item.split("=", 1)
                    meta_dict[key] = val
            return base, meta_dict

        return text.strip(), {}

    # TODO: i;plement validation
    # def validateDrones(self, nbDrones: str) -> int:
    #     pass

    # def validateStartHub(self, startHub: str) -> Zone:
    #     pass

    # def validateEndHub(self, endHub: str) -> Zone:
    #     pass

    # def validateHub(self, hub: str) -> Zone:
    #     pass

    # def validateConnection(self, connection: str) -> Connection:
    #     pass
