from .ble_helper import BleHelper
from .ble_remote_attribute_abstract import BleRemoteAttributeAbstract
from .ble_remote_descriptor import BleRemoteDescriptor


class BleRemoteCharacteristic(BleRemoteAttributeAbstract):
    def __init__(self, params):
        super().__init__(params)

        self.properties = params.get("properties", [])
        if type(self.properties) is not list:
            self.properties = [self.properties]

    @property
    def parent_name(self):
        return "service"

    @property
    def children_class(self):
        return BleRemoteDescriptor

    @property
    def children_name(self):
        return "descriptors"

    # addDescriptor(params) {
    #     return self.addChild(params)
    # }

    # //
    # // getCharacteristic(params) {
    # //   return self.getChild(params)
    # // }

    # getDescriptor(uuid) {
    #     let obj = self.getChild(uuid)
    #     if (obj) {
    #         return obj
    #     }
    #     let newCharacteristic = new BleRemoteDescriptor(self.obniz, self, uuid)
    #     self.addChild(newCharacteristic)
    #     return newCharacteristic
    # }

    # registerNotify(callback) {
    #     self.onnotify = callback
    #     obj = {
    #         "ble": {
    #             register_notify_characteristic: {
    #                 "address": self.get_service().get_peripheral().address,
    #                 "service_uuid": BleHelper.uuid_filter(self.get_service().uuid),
    #                 "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
    #             },
    #         },
    #     }
    #     self.get_service().get_peripheral().obniz.send(obj)
    # }

    # unregisterNotify() {
    #     self.onnotify = function() {}
    #     obj = {
    #         "ble": {
    #             unregister_notify_characteristic: {
    #                 "address": self.get_service().get_peripheral().address,
    #                 "service_uuid": BleHelper.uuid_filter(self.get_service().uuid),
    #                 "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
    #             },
    #         },
    #     }
    #     self.get_service().get_peripheral().obniz.send(obj)
    # }

    def read(self):
        obj = {
            "ble": {
                "read_characteristic": {
                    "address": self.get_service().get_peripheral().address,
                    "service_uuid": BleHelper.uuid_filter(self.get_service().uuid),
                    "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
                }
            }
        }
        self.get_service().get_peripheral().obniz.send(obj)

    def write(self, array, need_response=True):
        obj = {
            "ble": {
                "write_characteristic": {
                    "address": self.get_service().get_peripheral().address,
                    "service_uuid": BleHelper.uuid_filter(self.get_service().uuid),
                    "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
                    "data": array,
                    "needResponse": need_response,
                }
            }
        }
        self.get_service().get_peripheral().obniz.send(obj)

    def discover_children(self):
        obj = {
            "ble": {
                "get_descriptors": {
                    "address": self.get_service().get_peripheral().address,
                    "service_uuid": BleHelper.uuid_filter(self.get_service().uuid),
                    "characteristic_uuid": BleHelper.uuid_filter(self.uuid),
                }
            }
        }
        self.get_service().get_peripheral().obniz.send(obj)

    def discover_all_descriptors(self):
        return self.discover_children()

    # discoverAllDescriptorsWait() {
    #     return self.discoverChildrenWait()
    # }

    # toJSON() {
    #     let obj = super.toJSON()

    #     if (self.properties.length > 0) {
    #         obj.properties = self.properties
    #     }
    #     return obj
    # }

    # canBroadcast() {
    #     return self.properties.includes('broadcast')
    # }

    def can_notify(self):
        return "notify" in self.properties

    def can_read(self):
        return "read" in self.properties

    def can_write(self):
        return "write" in self.properties

    # canWriteWithoutResponse() {
    #     return self.properties.includes('write_without_response')
    # }

    def can_indicate(self):
        return "indicate" in self.properties

    def ondiscover(self, descriptor):
        self.ondiscoverdescriptor(descriptor)

    # ondiscoverfinished(descriptors) {
    #     self.ondiscoverdescriptorfinished(descriptors)
    # }

    def ondiscoverdescriptor(self, descriptor):
        pass

    # ondiscoverdescriptorfinished() {}

    # onregisternofity() {}

    # onunregisternofity() {}

    # onnotify() {}

    # notifyFromServer(notifyName, params) {
    #     super.notifyFromServer(notifyName, params)
    #     switch (notifyName) {
    #         case 'onregisternofity': {
    #             self.onregisternofity()
    #             break
    #         }
    #         case 'onunregisternofity': {
    #             self.onunregisternofity()
    #             break
    #         }
    #         case 'onnotify': {
    #             self.onnotify()
    #             break
    #         }
    #     }
    # }
