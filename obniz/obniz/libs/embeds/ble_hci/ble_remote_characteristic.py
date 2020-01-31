from .ble_remote_descriptor import BleRemoteDescriptor
from .ble_remote_attribute_abstract import BleRemoteAttributeAbstract
from .ble_helper import BleHelper

class BleRemoteCharacteristic(BleRemoteAttributeAbstract):
    def __init__(self, params):
        super().__init__(params)

        self.properties =  params.properties or []
        if not type(self.properties) is list:
            self.properties = [self.properties]

    ## def...
