from pathlib import Path
import sys
import pytest
from src.helper.parser import DataParser
from src.helper.pathfinding.path_finding import PathFinding
from src.helper.simulator import Simulator
from src.models.drone import Drone

# Ensure src is importable
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))


def simulate_map(map_file_path: Path) -> list[str]:
    parser = DataParser(str(map_file_path))
    map_obj = parser.parse_network_file()

    path_finding = PathFinding(map_obj)
    paths = path_finding.get_all_possible_paths()

    map_obj.paths = paths[:5]
    for path in map_obj.paths:
        path.zone_drones = {zone: [] for zone in path.zones}
        path.map = map_obj

    start_zone = map_obj.get_start_zone()
    path_count = min(5, len(map_obj.paths))
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

    counts = [int(map_obj.nbDrones * ratio) for ratio in chosen_ratios]
    remainder_drones = map_obj.nbDrones - sum(counts)
    counts[0] += remainder_drones

    drone_id = 1
    for path_index, count in enumerate(counts):
        assigned = []
        for _ in range(count):
            assigned.append(
                Drone(drone_id, map_obj.paths[path_index], start_zone)
            )
            drone_id += 1
        map_obj.paths[path_index].zone_drones[start_zone] = assigned
        map_obj.extendZoneDrones(start_zone, assigned)

    simulator = Simulator(map_obj)
    turns = simulator.run()
    return turns


@pytest.mark.parametrize(
    "relpath,target",
    [
        ("maps/easy/01_linear_path.txt", 6),
        ("maps/easy/02_simple_fork.txt", 8),
        ("maps/easy/03_basic_capacity.txt", 6),
        ("maps/medium/01_dead_end_trap.txt", 12),
        ("maps/medium/02_circular_loop.txt", 15),
        ("maps/medium/03_priority_puzzle.txt", 12),
        ("maps/hard/01_maze_nightmare.txt", 30),
        ("maps/hard/02_capacity_hell.txt", 35),
        ("maps/hard/03_ultimate_challenge.txt", 45),
        # challenger (optional)
        ("maps/challenger/01_the_impossible_dream.txt", 45),
    ],
)
def test_simulator_performance(relpath: str, target: int) -> None:
    map_path = project_root / relpath
    assert map_path.exists(), f"Map file not found: {map_path}"
    turns = simulate_map(map_path)
    assert isinstance(turns, list)
    assert (
        len(turns) <= target
    ), f"{relpath} exceeded target: {len(turns)} > {target}"
