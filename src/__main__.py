from pathlib import Path as FileSystemPath
from .helper.parser import DataParser
from .helper.exceptions import (
    ParsingException,
    PathFindingException,
    SimulationException,
)
from .models.map import Map
from .models.path import Path
from .helper.pathfinding import PathFinding
from .helper.simulator import Simulator
from .models.drone import Drone
import subprocess
from .helper.terminal import choose_map_file
from colorama import Fore, Style
from pathlib import Path as FilePath
from typing import List


def run_simulation_for_file(map_file: str) -> None:
    """parse given map, validate data and run simulation

    Args:
        map_file: map to execute

    Returns:
        None"""

    subprocess.call("clear")
    print(
        Fore.BLUE + Style.BRIGHT,
        "Selected map file: "
        + Fore.GREEN
        + f"{FilePath(map_file).name}{Fore.RESET}\n",
    )
    parser: DataParser = DataParser(map_file)

    map: Map
    map = parser.parse_network_file()

    path_finding: PathFinding = PathFinding(map)
    paths: list[Path] = path_finding.get_all_possible_paths()

    map.paths = paths[:5]
    for path in map.paths:
        path.zone_drones = {zone: [] for zone in path.zones}
        path.map = map

    start_zone = map.get_start_zone()
    path_count = min(5, len(map.paths))

    if path_count == 0:
        raise ValueError("No valid path found for the current map.")

    ratios = {
        1: [1.0],
        2: [0.7, 0.3],
        3: [0.5, 0.25, 0.25],
        4: [0.25, 0.25, 0.25, 0.25],
        5: [0.2, 0.2, 0.2, 0.2, 0.2],
    }
    chosen_ratios = ratios.get(path_count, [1.0 / path_count] * path_count)

    # find the number of drones to split on paths
    counts = [int(map.nbDrones * ratio) for ratio in chosen_ratios]

    # add the remainder number of drones to the first path
    remainder_drones = map.nbDrones - sum(counts)
    counts[0] += remainder_drones

    drones_by_path: list[list[Drone]] = []
    drone_id = 1

    # start assigning drones to paths
    for path_index, count in enumerate(counts):
        assigned: List[Drone] = []
        for _ in range(count):
            assigned.append(Drone(drone_id, map.paths[path_index], start_zone))
            drone_id += 1
        drones_by_path.append(assigned)
        # dispatch drones on start zone for every path
        map.paths[path_index].zone_drones[start_zone] = assigned
        map.extendZoneDrones(start_zone, assigned)

    simulator: Simulator = Simulator(map)
    result: List[str] = simulator.run()
    print(
        Fore.BLUE
        + " Total drones: "
        + Fore.GREEN
        + f"{map.nbDrones}"
        + Fore.WHITE
    )
    print(
        Fore.BLUE
        + " Total turns: "
        + Fore.GREEN
        + f"{len(result)}\n"
        + Fore.WHITE
    )
    for t in result:
        print(t)


def main() -> None:
    while True:
        try:
            project_root = FileSystemPath(__file__).resolve().parent.parent
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
