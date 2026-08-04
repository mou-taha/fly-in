from models.map import Map
from models.path import Path
from typing import List


class Simulator:
    def __init__(self, map: Map, paths: List[Path]):
        self.map = map
        self.paths = paths
