from .ble_attribute_abstract import BleAttributeAbstract
from .ble_helper import BleHelper


class BleDescriptor(BleAttributeAbstract):
    def __init__(self, obj):
        super().__init__(obj)

        self.permissions = obj.get("permissions", [])
        if type(self.permissions) is not list:
            self.permissions = [self.permissions]

    @property
    def parent_name(self):
        return "characteristic"

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

    # toJSON() {
    #     let obj = super.toJSON()

    #     if (self.permissions.length > 0) {
    #         obj.permissions = self.permissions
    #     }
    #     return obj
    # }

    def write(self, data_array, need_response=False):
        self.get_characteristic().get_service().peripheral.obniz.send(
            {
                "ble": {
                    "peripheral": {
                        "write_descriptor": {
                            "service_uuid": BleHelper.uuid_filter(
                                self.get_characteristic().get_service().uuid
                            ),
                            "characteristic_uuid": BleHelper.uuid_filter(
                                self.get_characteristic().uuid
                            ),
                            "descriptor_uuid": self.uuid,
                            "data": data_array,
                        }
                    }
                }
            }
        )

    def read(self):
        self.get_characteristic().get_service().peripheral.obniz.send(
            {
                "ble": {
                    "peripheral": {
                        "read_descriptor": {
                            "service_uuid": BleHelper.uuid_filter(
                                self.get_characteristic().get_service().uuid
                            ),
                            "characteristic_uuid": BleHelper.uuid_filter(
                                self.get_characteristic().uuid
                            ),
                            "descriptor_uuid": self.uuid,
                        }
                    }
                }
            }
        )
