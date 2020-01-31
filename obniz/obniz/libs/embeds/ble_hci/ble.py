from .hci import ObnizBLEHci
from .protocol.central.bindings import NobleBindings
from .protocol.peripheral.bindings import BlenoBindings
from .protocol.hci import Hci as HciProtocol
from .ble_helper import BleHelper

from .ble_peripheral import BlePeripheral
from .ble_service import BleService
from .ble_characteristic import BleCharacteristic
from .ble_descriptor import BleDescriptor
from .ble_remote_peripheral import BleRemotePeripheral
from .ble_advertisement import BleAdvertisement
from .ble_scan import BleScan
from .ble_security import BleSecurity

class ObnizBLE:
    def __init__(self, obniz):
        self.obniz = obniz
        self.hci = ObnizBLEHci(obniz)
        self.hci_protocol = HciProtocol(self.hci)

        self.central_bindings = NobleBindings(self.hci_protocol)
        self.peripheral_bindings = BlenoBindings(self.hci_protocol)

        self.peripheral_bindings.init()
        self.peripheral_bindings.init()

        self._initialized = False

        self.remote_peripherals = []

        self.service = BleService
        self.characteristic = BleCharacteristic
        self.descriptor = BleDescriptor
        self.peripheral = BlePeripheral(self)

        self.scanTarget = None

        self.advertisement = BleAdvertisement(self)
        self.scan = BleScan(self)
        self.security = BleSecurity(self)

        self._bind()
        self._reset()

    async def init_wait(self):
        if not self._initialized:
            self.initialized = True
            await self.hci_protocol.init_wait()

    def notified(self, obj):
        if "hci" in obj:
            self.hci.notified(obj["hci"])

    def _reset(self):
        pass

    ## def...

    def onStateChange(self):
        pass
    def onAddressChange(self):
        pass

    def onScanStart(self):
        pass

    def onScanStop(self):
        # this.scan.notifyFromServer('onfinish')
        pass

    # # def...

    def onPeripheralStateChange(self):
        pass

    def onPeripheralAddressChange(self):
        pass

    # # def...

    def _bind(self):
        @self.central_bindings.ee.on('stateChange')
        def onStateChange(state):
            self.onStateChange()

        @self.central_bindings.ee.on('addressChange')
        def onAddressChange(address):
            self.onAddressChange()

        @self.central_bindings.ee.on('scanStart')
        def onScanStart(filterDuplicates):
            self.onScanStart(filterDuplicates)

        @self.peripheral_bindings.ee.on('stateChange')
        def onPeripheralStateChange(state):
            self.onPeripheralStateChange()
        @self.peripheral_bindings.ee.on('addressChange')
        def onPeripheralAddressChange(address):
            self.onPeripheralAddressChange()
