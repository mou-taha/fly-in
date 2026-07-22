from .zone import Zone


class Map:
    def __init__(self, nbDrones: int, zones: set[Zone]):
        self.nbDrones = nbDrones
        self.zones = zones
