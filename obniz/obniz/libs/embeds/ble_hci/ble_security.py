from pyee import EventEmitter
import semver

class BleSecurity:
    ee = EventEmitter()

    def __init__(self, Obniz):
        self.Obniz = Obniz

    ## def...