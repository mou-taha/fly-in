from .zone import Zone


class Space:
    def __init__(self, zones: set[Zone]):
        self.zones = zones
