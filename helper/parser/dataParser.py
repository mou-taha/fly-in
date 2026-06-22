from models.zone import Zone
from models.connection import Connection
from .input import Input
from ..exceptions.parsingException import ParsingException


class DataParser:
    def __init__(self) -> None:
        pass

    def parseData(self, filePath: str) -> Input:
        data: Input = Input()

        with open(filePath, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    if "nb_drones" not in key:
                        raise ParsingException("nb_drones must be at",
                                               "the first line")
                    if key == "nb_drones":
                        data.nbDrones = int(value)
                    elif key == "start_hub":
                        data.startHub = value
                    elif key == "end_hub":
                        data.endHub = value
                    elif key == "hub":
                        data.hubs.append(value)
                    elif key == "connection":
                        data.connections.append(value)
        return data

    def validateDrones(self, nbDrones: str) -> int:
        pass

    def validateStartHub(self, startHub: str) -> Zone:
        pass

    def validateEndHub(self, endHub: str) -> Zone:
        pass

    def validateHub(self, hub: str) -> Zone:
        pass

    def validateConnection(self, connection: str) -> Connection:
        pass
