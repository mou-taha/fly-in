from pathlib import Path as FileSystemPath
from helper.parser.dataParser import DataParser
from helper.exceptions.parsingException import ParsingException
from helper.exceptions.path_finding_exception import PathFindingException
from helper.exceptions.simulation_exception import SimulationException
from models.map import Map
from models.path import Path
from helper.pathfinding.path_finding import PathFinding
from models.simulator import Simulator
from models.drone import Drone
import subprocess
from helper.terminal.terminal import choose_map_file
from colorama import Fore, Style
from pathlib import Path as FilePath
from typing import List


def run_simulation_for_file(map_file: str) -> None:

    subprocess.call("clear")
    print(
        Fore.BLUE + Style.BRIGHT,
        f"Selected map file: {Fore.GREEN}{FilePath(map_file).name}{Fore.RESET}\n",
    )
    parser: DataParser = DataParser(map_file)

    map: Map
    map = parser.parse_network_file()

    path_finding: PathFinding = PathFinding(map)
    paths: list[Path] = path_finding.get_all_possible_paths()

    map.paths = paths[:2]
    for path in map.paths:
        path.zone_drones = {zone: [] for zone in path.zones}
        path.map = map

    start_zone = map.get_start_zone()
    if len(map.paths) > 1:
        amount_1 = map.nbDrones // 2
        dlist0 = [
            Drone(index + 1, map.paths[0], start_zone)
            for index in range(amount_1)
        ]
        dlist1 = [
            Drone(index + 1, map.paths[1], start_zone)
            for index in range(amount_1, map.nbDrones)
        ]
        map.paths[0].zone_drones[start_zone] = dlist0
        map.paths[1].zone_drones[start_zone] = dlist1
        map.extendZoneDrones(start_zone, dlist0)
        map.extendZoneDrones(start_zone, dlist1)
    else:
        dlist = [
            Drone(index + 1, map.paths[0], start_zone)
            for index in range(map.nbDrones)
        ]
        map.paths[0].zone_drones[start_zone] = dlist
        map.extendZoneDrones(start_zone, dlist)

    simulator: Simulator = Simulator(map)
    result: List[str] = simulator.run()
    print(
        Fore.BLUE
        + " Total turns: "
        + Fore.GREEN
        + f"{len(result)}\n"
        + Fore.WHITE
    )
    for t in result:
        print(t)


def main():
    project_root = FileSystemPath(__file__).resolve().parent
    while True:
        try:
            map_file = choose_map_file(project_root)
            if map_file is None:
                print("Goodbye.")
                break
            run_simulation_for_file(map_file)
            print(
                Fore.CYAN
                + "\n menu reopened. Choose another file or exit.\n"
                + Fore.WHITE
            )
        except (
            FileNotFoundError,
            ValueError,
            ParsingException,
            PathFindingException,
            SimulationException,
            Exception,
        ) as e:
            print(e)
            print("\nReturning to the menu...\n")


if __name__ == "__main__":
    main()
