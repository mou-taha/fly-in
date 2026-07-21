from models.zone import Zone, ZoneType
from models.connection import Connection
from models.space import Space
from typing import Any, List
from ..exceptions.parsingException import ParsingException
import re


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

        with open(self.filePath, "r") as file:
            fileLines: List[str] = file.readlines()
            lineValidations: List[str] = self.validate_lines(fileLines)
            if len(lineValidations) > 0:
                raise ParsingException("\n".join(lineValidations))
            for index, line in enumerate(fileLines):
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
                    nb_drones = int(value)
                elif key in ("hub", "start_hub", "end_hub"):
                    keyCounter += 1
                    # 1. Extract metadata
                    base_text, meta_dict = self.extract_metadata(value)

                    # 2. Parse base text: "name x y"
                    parts = base_text.split()
                    name = parts[0]
                    try:
                        x = int(parts[1])
                        y = int(parts[2])
                    except (ValueError, IndexError):
                        raise ParsingException(
                            f"line {index+1}: the zone coordinate must be "
                            "a valid integer."
                        )
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
                        zoneType=zone_type,
                    )
                    zones_dict[name] = zone

                elif key == "connection":
                    keyCounter += 1
                    # save connections to process after all zones are created
                    connections_data.append(value)

                if keyCounter >= 1 and nb_drones == -1:
                    raise ParsingException(
                        "The first line must define "
                        "the number of drones using "
                        "nb_drones: <positive_integer>."
                    )

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
                    zoneA.connections.append(
                        Connection(zone=zoneB, maxLinkCapacity=capacity)
                    )
                    zoneB.connections.append(
                        Connection(zone=zoneA, maxLinkCapacity=capacity)
                    )

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

    def validate_lines(self, lines: List[str]) -> List[str]:
        result: List[str] = []
        for index, raw_line in enumerate(lines):
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue

            if ":" not in line:
                result.append(
                    f'line {index+1}: missing ":" separator\n  {raw_line.strip()}'
                )
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "nb_drones":
                error = self._validate_nb_drones(value)
            elif key in ("hub", "start_hub", "end_hub"):
                error = self._validate_zone_line(key, value)
            elif key == "connection":
                error = self._validate_connection_line(value)
            else:
                error = f'unknown key "{key}".'

            if error:
                result.append(f'line {index+1}: {error}\n  {raw_line.strip()}')

        return result

    def _validate_nb_drones(self, value: str) -> str | None:
        if not value:
            return "nb_drones requires a positive integer value."
        if not re.fullmatch(r"\d+", value):
            return "nb_drones must be a positive integer."
        return None

    def _validate_zone_line(self, key: str, value: str) -> str | None:
        base_text, meta_dict = self.extract_metadata(value)
        parts = base_text.split()
        if len(parts) < 3:
            return f'{key} must be followed by "name x y".'

        name, x_text, y_text = parts[0], parts[1], parts[2]
        if not name:
            return "zone name is missing."

        if not re.fullmatch(r"-?\d+", x_text):
            return f'x coordinate "{x_text}" must be an integer.'
        if not re.fullmatch(r"-?\d+", y_text):
            return f'y coordinate "{y_text}" must be an integer.'

        for meta_key, meta_value in meta_dict.items():
            if meta_key == "color":
                if not re.fullmatch(r"[A-Za-z]+", meta_value):
                    return f'color value "{meta_value}" must contain only letters.'
            elif meta_key == "max_drones":
                if not re.fullmatch(r"\d+", meta_value):
                    return f'max_drones value "{meta_value}" must be a positive integer.'
            elif meta_key == "zone":
                if meta_value.lower() not in {"normal", "blocked", "restricted", "priority"}:
                    return (
                        f'zone value "{meta_value}" must be one of normal, blocked, restricted, priority.'
                    )
            else:
                return f'unknown metadata key "{meta_key}".'

        return None

    def _validate_connection_line(self, value: str) -> str | None:
        base_text, meta_dict = self.extract_metadata(value)
        if "-" not in base_text:
            return 'connection must be formatted as "zoneA-zoneB".'

        name1, name2 = base_text.split("-", 1)
        if not name1 or not name2:
            return "connection must include two zone names."
        if " " in name1 or " " in name2:
            return "connection zone names may not contain spaces."

        for meta_key, meta_value in meta_dict.items():
            if meta_key == "max_link_capacity":
                if not re.fullmatch(r"\d+", meta_value):
                    return f'max_link_capacity value "{meta_value}" must be a positive integer.'
            else:
                return f'unknown metadata key "{meta_key}".'

        return None