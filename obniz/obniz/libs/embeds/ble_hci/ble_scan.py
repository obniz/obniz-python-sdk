
# from eventemitter3 import emitter

class BleScan:
    def __init__(self, obnizBle):
        self.scan_target = None
        self.obnizBle = obnizBle

        self.scanned_peripherals = []

    def start(self, target, settings):
        print("SCAN!")

    ## def...

    def onfind(self):
        pass