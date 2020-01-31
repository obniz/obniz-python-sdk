from .ble_helper import BleHelper
from .ble_attribute_abstract import BleAttributeAbstract

class BleLocalAttributeAbstract(BleAttributeAbstract):
    def __init__(self, params):
        super.__init__(params)

        self.RESULT_SUCCESS = 0x00
        self.RESULT_INVALID_OFFSET = 0x07
        self.RESULT_ATTR_NOT_LONG = 0x0b
        self.RESULT_INVALID_ATTRIBUTE_LENGTH = 0x0d
        self.RESULT_UNLIKELY_ERROR = 0x0e

    ## def...
