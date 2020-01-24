from .hci import ObnizBLEHci


from .protocol.hci import Hci as HciProtocol
# ###

# from .ble_peripheral import BlePeripheral
# from .ble_service import BleService
# from .ble_characteristic import BleCharacteristic
# from .ble_descriptor import BleDescriptor
# from .ble_remote_peripheral import BleRemotePeripheral
# from .ble_advertisement import BleAdvertisement
from .ble_scan import BleScan
# from .ble_security import BleSecurity

class ObnizBLE:
    def __init__(self, obniz):
        self.obniz = obniz
        self.hci = ObnizBLEHci(obniz)
        self.hci_protocol = HciProtocol(self.hci)

        self._initialized = False

        ##

        self.scan = BleScan(self)

    async def init_wait(self):
        if not self._initialized:
            self.initialized = True
            await self.hci_protocol.init_wait()

    def notified(self, obj):
        if "hci" in obj:
            self.hci.notified(obj["hci"])
