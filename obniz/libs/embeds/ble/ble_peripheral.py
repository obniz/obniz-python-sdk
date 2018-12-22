from .ble_helper import BleHelper
from .ble_service import BleService


class BlePeripheral:
    def __init__(self, obniz):
        self.obniz = obniz
        self.services = []

    def add_service(self, obj):
        if not isinstance(obj, BleService):
            obj = BleService(obj)

        self.services.append(obj)
        obj.peripheral = self
        self.obniz.send({"ble": {"peripheral": {"services": [obj]}}})

    def set_json(self, json):
        if "services" in json:
            for service in json["services"]:
                self.add_service(service)

    def get_service(self, uuid):
        uuid = BleHelper.uuid_filter(uuid)
        return next(
            iter(
                [
                    element
                    for element in self.services
                    if BleHelper.uuid_filter(element.uuid) == uuid
                ]
            ),
            None,
        )

    # removeService(uuid) {
    #     self.services = self.services.filter(function(element) {
    #         return BleHelper.uuid_filter(element.uuid) !== uuid
    #     })
    # }

    # stopAllService() {
    #     self.obniz.send({
    #         "ble": {
    #              "peripheral": null,
    #         },
    #     })
    #     self.services = []
    # }

    def to_json(self):
        return {"services": self.services}

    def find_characteristic(self, param):
        service_uuid = BleHelper.uuid_filter(param["service_uuid"])
        characteristic_uuid = BleHelper.uuid_filter(param["characteristic_uuid"])
        s = self.get_service(service_uuid)
        if s:
            return s.get_characteristic(characteristic_uuid)

        return None

    def find_descriptor(self, param):
        descriptor_uuid = BleHelper.uuid_filter(param["descriptor_uuid"])
        c = self.find_characteristic(param)
        if c:
            return c.get_descriptor(descriptor_uuid)

        return None

    def end(self):
        self.obniz.send({"ble": {"peripheral": None}})

    # onconnectionupdates() {}

    # onerror() {}
