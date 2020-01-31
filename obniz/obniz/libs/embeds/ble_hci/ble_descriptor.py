from .ble_local_attribute_abstract import BleLocalAttributeAbstract

class BleDescriptor(BleLocalAttributeAbstract):
    def __init__(self, obj):
        super().__init__(obj)

        self.permissions = obj.permissions or []
        if not type(self.permissions) is list:
            self.permissions = [self.permissions]

    ## def...
