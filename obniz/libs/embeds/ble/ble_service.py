from .ble_attribute_abstract import BleAttributeAbstract
from .ble_characteristic import BleCharacteristic

# const BleHelper = require('./bleHelper')


class BleService(BleAttributeAbstract):
    def __init__(self, obj):
        super().__init__(obj)

        self.add_characteristic = self.add_child
        self.get_characteristic = self.get_child

    @property
    def parent_name(self):
        return "peripheral"

    @property
    def children_name(self):
        return "characteristics"

    @property
    def children_class(self):
        return BleCharacteristic

    @property
    def adv_data(self):
        return {
            "flags": ["general_discoverable_mode", "br_edr_not_supported"],
            "serviceUuids": [self.uuid],
        }

    # end() {
    #     self.peripheral.Obniz.send({
    #         ble: {
    #             peripheral: {
    #                 stop_service: {
    #                     service_uuid: BleHelper.uuidFilter(self.uuid),
    #                 },
    #             },
    #         },
    #     })
    #     self.peripheral.removeService(self.uuid)
    # }

    # notify(notifyName, params) {
    #     //nothing
    # }
