from .ble_attribute_abstract import BleAttributeAbstract

class BleRemoteAttributeAbstract(BleAttributeAbstract):
    def __init__(self, params):
        super.__init__(params)

        self.is_remote = False
        self.deicover_on_remote = False

    ## def...
