*This project has been created as part of the 42 curriculum by tmousnia.*

# Description

This project is a drone routing and simulation system developed in Python. It reads a map description, builds a network of connected zones, computes possible paths, and simulates the movement of multiple drones while respecting the map constraints and the routing logic.

The objective is to model a delivery or exploration scenario where several drones must traverse the same environment efficiently. The application focuses on:

- parsing custom map files
- building a graph of zones and connections
- finding valid paths through the network
- distributing drones across the best route candidates
- running a turn-based simulation until all drones complete their mission

This is a classic pathfinding and simulation problem adapted to a 42 project format, combining graph traversal, constraints management, and procedural execution.

# Project Structure

- `main.py`: entry point of the application
- `models/`: simulation domain objects such as map, zones, drones, paths, and simulator
- `helper/`: parsing, pathfinding, and terminal interaction utilities
- `maps/`: example map files used to test the solver and simulation engine

# Instructions

## Prerequisites

- Python 3.10 or later
- `pip` or `uv` for dependency installation

## Installation

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pydantic simple-term-menu rich
```

If you prefer the project-managed environment workflow, this repository also includes a `pyproject.toml` configuration that can be used with `uv`:

```bash
uv sync
```

## Running the Program

Start the simulator from the repository root:

```bash
python main.py
```

A menu will appear and let you choose one of the provided map files or enter a custom path. The program will parse the map, compute routes, assign drones, and run the simulation.

## Example Maps

The `maps/` directory contains several sample scenarios, including easy, medium, hard, and challenger levels. These can be used to test different pathfinding and coordination behaviors.

# Resources

## Classic References

- [Python official documentation](https://docs.python.org/3/)
- [Graph theory and pathfinding references](https://en.wikipedia.org/wiki/Graph_theory)
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)

These resources are relevant because the project relies on graph-based route planning and simulation behavior comparable to shortest-path and constrained traversal problems.

## AI Usage

AI tools were used as support during development for:

- explaining algorithmic concepts and project structure
- helping review code organization and identify edge cases in the pathfinding logic
- drafting and improving the documentation and project README
- suggesting ways to structure validation and simulation flow

The AI was not used to replace the core project design; the actual routing logic, map parsing, and simulation behavior were implemented and validated by the project author.

# Notes

This project is designed as a compact but complete challenge simulation: it combines data parsing, graph exploration, path selection, and turn-based execution in a single system. It is intended to be easy to run locally, while still supporting custom maps and more advanced route planning experiments.