from .ble_helper import BleHelper
from .ble_remote_attribute_abstract import BleRemoteAttributeAbstract


class BleRemoteDescriptor(BleRemoteAttributeAbstract):
    def __init__(self, params):
        super().__init__(params)

    @property
    def parent_name(self):
        return "characteristic"

    def read(self):
        obj = {
            "ble": {
                "read_descriptor": {
                    "address": self.get_characteristic()
                    .get_service()
                    .get_peripheral()
                    .address,
                    "service_uuid": BleHelper.uuid_filter(
                        self.get_characteristic().get_service().uuid
                    ),
                    "characteristic_uuid": BleHelper.uuid_filter(
                        self.get_characteristic().uuid
                    ),
                    "descriptor_uuid": BleHelper.uuid_filter(self.uuid),
                }
            }
        }
        self.get_characteristic().get_service().get_peripheral().obniz.send(obj)

    def write(self, array, need_response=True):
        obj = {
            "ble": {
                "write_descriptor": {
                    "address": self.get_characteristic()
                    .get_service()
                    .get_peripheral()
                    .address,
                    "service_uuid": BleHelper.uuid_filter(
                        self.get_characteristic().get_service().uuid
                    ),
                    "characteristic_uuid": BleHelper.uuid_filter(
                        self.get_characteristic().uuid
                    ),
                    "descriptor_uuid": BleHelper.uuid_filter(self.uuid),
                    "data": array,
                    "needResponse": need_response,
                }
            }
        }
        self.get_characteristic().get_service().get_peripheral().obniz.send(obj)
