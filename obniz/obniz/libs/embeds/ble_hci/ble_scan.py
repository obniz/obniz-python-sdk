
# from eventemitter3 import emitter

class BleScan:
    def __init__(self, obnizBle):
        self.scanTarget = None
        self.obnizBle = obnizBle
        # self.emitter = emitter()

        self.scannedPeripherals = []

    def start(self, target, settings):
        print("SCAN!")