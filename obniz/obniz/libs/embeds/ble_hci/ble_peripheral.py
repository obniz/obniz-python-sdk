from .ble_service import BleService
from .ble_helper import BleHelper

class BlePeripheral():
    def __init__(self, obnizBle):
        self.obnizBle = obnizBle
        self.services = []
        self.current_connected_device_address = None

    ## def...
