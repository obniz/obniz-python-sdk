from .ble_helper import BleHelper
from .ble_remote_attribute_abstract import BleRemoteAttributeAbstract
from .ble_remote_characteristic import BleRemoteCharacteristic


class BleRemoteService(BleRemoteAttributeAbstract):
    def __init__(self, obj):
        super().__init__(obj)

    @property
    def parent_name(self):
        return "peripheral"

    @property
    def children_class(self):
        return BleRemoteCharacteristic

    @property
    def children_name(self):
        return "characteristics"

    # def addCharacteristic(self, params):
    #     return self.addChild(params)

    # getCharacteristic(params) {
    #     return self.getChild(params)
    # }

    def discover_all_characteristics(self):
        return self.discover_children()

    # discoverAllCharacteristicsWait() {
    #     return self.discover_childrenWait()
    # }

    def discover_children(self):
        obj = {
            "ble": {
                "get_characteristics": {
                    "address": self.get_peripheral().address,
                    "service_uuid": BleHelper.uuid_filter(self.uuid),
                }
            }
        }
        self.parent.obniz.send(obj)

    def ondiscover(self, characteristic):
        self.ondiscovercharacteristic(characteristic)

    # ondiscoverfinished(characteristics) {
    #     self.ondiscovercharacteristicfinished(characteristics)
    # }

    def ondiscovercharacteristic(self, characteristic):
        pass

    # ondiscovercharacteristicfinished() {}
