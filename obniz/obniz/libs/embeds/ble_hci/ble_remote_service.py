from .ble_remote_characteristic import BleRemoteCharacteristic
from .ble_remote_attribute_abstract import BleRemoteAttributeAbstract
from .ble_helper import BleHelper

class BleRemoteService(BleRemoteAttributeAbstract):
    def __init__(self, obj):
        super().__init__(obj)

    ## def...