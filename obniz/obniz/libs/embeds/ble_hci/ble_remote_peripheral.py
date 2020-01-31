from pyee import EventEmitter
from .ble_remote_service import BleRemoteService
from .ble_helper import BleHelper

class BleRemotePeripheral:
    ee = EventEmitter()
    def __init__(self, obnizBle, address):
        self.obnizBle = obnizBle
        self.address = address
        self.connected = False

        self.device_type = None
        self.address_type = None
        self.ble_event_type = None
        self.rssi = None
        self.adv_data = None
        self.scan_resp = None

        self.keys = [
            'device_type',
            'address_type',
            'ble_event_type',
            'rssi',
            'adv_data',
            'scan_resp',
        ]

        self.services = []

    ## def...