from .zone import Zone


class Space:
    def __init__(self, nbDrones: int, zones: set[Zone]):
        self.nbDrones = nbDrones
        self.zones = zones
