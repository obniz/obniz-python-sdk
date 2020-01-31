from .ble_helper import BleHelper

class BleAdvertisementBuilder:
    def __init__(self, Obniz, json):
        self.Obniz = Obniz
        self.rows = {}

        if json:
            if 'localName' in json:
                self.set_complete_local_name(json.localName)
            if 'manufacturerData' in json:
                if 'companyCode' in json.manufacturerData and 'manufacturerData' in json.manufacturereData:
                    self.set_manufacturer_specific_data(json.manufacturerData.companyCode, json.manufacturerData.data)
            if 'serviceUuids' in json:
                for uuid in json.serviceUuids:
                    self.set_uuid(uuid)
        if callable(self.extend_eval_json):
            self.extend_eval_json(json)

    def extend_eval_json(self, json):
        print("wip: extend_eval_json")

    ## def...