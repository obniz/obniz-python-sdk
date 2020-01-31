from .ble_advertisement_builder import BleAdvertisementBuilder

class BleAdvertisement:
    def __init__(self, obnizBle):
        self.obnizBle = obnizBle
        self.adv_data = []
        self.scan_resp = []

    ## def...