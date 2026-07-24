from models.zone import Zone


class Connection:

    def __init__(self, zone: Zone, maxLinkCapacity: int):
        self.zone = zone
        self.maxLinkCapacity = maxLinkCapacity
