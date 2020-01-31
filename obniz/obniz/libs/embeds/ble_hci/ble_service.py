from .ble_local_attribute_abstract import BleLocalAttributeAbstract
from .ble_characteristic import BleCharacteristic
from .ble_helper import BleHelper

class BleService(BleLocalAttributeAbstract):
    def __init__(self, obj):
        super().__init__(obj)

        self.add_characteristic = self.add_child
        self.get_Characteristic = self.get_child

    @property
    def parent_name(self):
        return 'peripheral'

    ## def...
