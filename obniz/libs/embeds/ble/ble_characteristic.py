from .ble_attribute_abstract import BleAttributeAbstract
from .ble_descriptor import BleDescriptor
from .ble_helper import BleHelper


class BleCharacteristic(BleAttributeAbstract):
    def __init__(self, obj):
        super().__init__(obj)

        self.add_descriptor = self.add_child
        self.get_descriptor = self.get_child

        self.properties = obj.get("properties", [])
        if type(self.properties) is not list:
            self.properties = [self.properties]

        self.permissions = obj.get("permissions", [])
        if type(self.permissions) is not list:
            self.permissions = [self.permissions]

    @property
    def parent_name(self):
        return "service"

    @property
    def children_class(self):
        return BleDescriptor

    @property
    def children_name(self):
        return "descriptors"

    # toJSON() {
    #     let obj = super.toJSON()

    #     if (self.properties.length > 0) {
    #         obj.properties = self.properties
    #     }

    #     if (self.permissions.length > 0) {
    #         obj.permissions = self.permissions
    #     }
    #     return obj
    # }

    # addProperty(param) {
    #     if (!self.properties.includes(param)) {
    #         self.properties.push(param)
    #     }
    # }

    # removeProperty(param) {
    #     self.properties = self.properties.filter(elm => {
    #         return elm !== param
    #     })
    # }

    # addPermission(param) {
    #     if (!self.permissions.includes(param)) {
    #         self.permissions.push(param)
    #     }
    # }

    # removePermission(param) {
    #     self.permissions = self.permissions.filter(elm => {
    #         return elm !== param
    #     })
    # }

    def write(self, data, need_response=False):
        self.get_service().peripheral.obniz.send(
            {
                "ble": {
                    "peripheral": {
                        "write_characteristic": {
                            "service_uuid": BleHelper.uuid_filter(
                                self.get_service().uuid
                            ),
                            "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
                            "data": data,
                        }
                    }
                }
            }
        )

    def read(self):
        self.get_service().peripheral.obniz.send(
            {
                "ble": {
                    "peripheral": {
                        "read_characteristic": {
                            "service_uuid": BleHelper.uuid_filter(
                                self.get_service().uuid
                            ),
                            "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
                        }
                    }
                }
            }
        )

    # notify() {
    #     self.get_service().peripheral.Obniz.send({
    #         "ble": {
    #             "peripheral": {
    #                 notify_characteristic: {
    #                     "service_uuid": BleHelper.uuid_filter(self.get_service().uuid),
    #                     "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
    #                 },
    #             },
    #         },
    #     })
    # }
