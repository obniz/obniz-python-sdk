from .ble_advertisement_builder import BleAdvertisementBuilder as Builder


class BleAdvertisement:
    def __init__(self, obniz):
        self.obniz = obniz
        self.adv_data = []
        self.scan_resp = []

    def start(self):
        obj = {}
        obj["ble"] = {}
        obj["ble"]["advertisement"] = {"adv_data": self.adv_data}

        if len(self.scan_resp) > 0:
            obj["ble"]["advertisement"]["scan_resp"] = self.scan_resp

        self.obniz.send(obj)

    def end(self):
        obj = {}
        obj["ble"] = {}
        obj["ble"]["advertisement"] = None
        self.obniz.send(obj)

    def set_adv_data_raw(self, adv_data):
        self.adv_data = adv_data

    def set_adv_data(self, json):
        builder = self.adv_data_bulider(json)
        self.set_adv_data_raw(builder.build())

    def adv_data_bulider(self, json_val):
        return Builder(self.obniz, json_val)

    def scan_resp_data_builder(self, json):
        return Builder(self.obniz, json)

    def set_scan_resp_data_raw(self, scan_resp):
        self.scan_resp = scan_resp

    def set_scan_resp_data(self, json):
        self.set_scan_resp_data_raw(self.scan_resp_data_builder(json).build())
