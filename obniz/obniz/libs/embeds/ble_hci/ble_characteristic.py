from .ble_descriptor import BleDescriptor
from .ble_local_attribute_abstract import BleLocalAttributeAbstract

class BleCharacteristic(BleLocalAttributeAbstract):
    def __init(self, obj):
        super().__init__(obj)

        self._max_value_size = None
        self._update_value_callback = None

        self.add_descriptor = self.add_child
        self.get_descriptor = self.get_child

        self.properties = params.properties or []
        if not type(self.properties) is list:
            self.properties = [self.properties]


        self.permissions = obj.permissions or []
        if not type(self.permissions) is list:
            self.permissions = [self.permissions]

    ## def...
