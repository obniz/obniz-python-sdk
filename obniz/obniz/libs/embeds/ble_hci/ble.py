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

        self.central_bindings.init()
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

    def find_peripheral(self, address):
        for remote_peripheral in self.remote_peripherals:
            if remote_peripheral.address == address:
                return remote_peripheral
        return None

    ## def...

    def on_state_change(self):
        pass
    def on_address_change(self):
        pass

    def on_scan_start(self, filter_duplicates):
        pass
    
    def on_scan_stop(self):
        print("wip: on_scan_stop")
        # this.scan.notifyFromServer('onfinish')

    def on_discover(self, uuid, address, address_type, connectable, advertisement, rssi):
        val = self.find_peripheral(uuid)

        if not val:
            val = BleRemotePeripheral(self, uuid)
            self.remote_peripherals.append(val)
        val.discoverd_on_remote = True

        peripheral_data = {
            'device_type': "ble",
            'address_type': address_type,
            'ble_event_type': "connectable_advertisemnt" if connectable else "non_connectable_advertising",
            'rssi': rssi,
            'adv_data': advertisement["advertisementRaw"],
            'scan_resp': advertisement["scanResponseRaw"],
        }
        val.set_params(peripheral_data)
        val._adv_data_filtered = advertisement

        self.scan.notify_from_server('onfind', val)

    def on_connect(self):
        print("wip: on_connect")

    def on_disconnect(self):
        print("wip: on_disconnect")

    def on_rssi_update(self):
        pass

    def on_services_discover(self):
        print("wip: on_services_discover")
        
    def on_included_services_discover(self):
        pass

    def on_characteristics_discover(self):
        print("wip: on_characteristics_discover")


    def on_read(self):
        print("wip: on_read")

    def on_write(self):
        print("wip: on_write")

    def on_broadcast(self):
        pass

    def on_notify(self):
        print("wip: on_notify")

    def on_descriptors_discover(self):
        print("wip: on_descriptors_discover")

    def on_value_read(self):
        print("wip: on_value_read")

    def on_value_write(self):
        print("wip: on_value_write")

    def on_handle_read(self):
        pass
    def on_handle_write(self):
        pass
    def on_handle_notify(self):
        pass


    def on_peripheral_state_change(self):
        pass

    def on_peripheral_address_change(self):
        pass

    # # def...

    def _bind(self):

        @self.central_bindings.ee.on('state_change')
        def on_state_change(state):
            self.on_state_change()

        @self.central_bindings.ee.on('address_change')
        def on_address_change(address):
            self.on_address_change()

        @self.central_bindings.ee.on('scan_start')
        def on_scan_start(filter_duplicates):
            self.on_scan_start(filter_duplicates)
        @self.central_bindings.ee.on('scan_stop')
        def on_scan_stop():
            self.on_scan_stop()
        @self.central_bindings.ee.on('discover')
        def on_discover(uuid, address, address_type, connectable, advertisement, rssi):
            self.on_discover(uuid, address, address_type, connectable, advertisement, rssi)
        @self.central_bindings.ee.on('connect')
        def on_connect():
            self.on_connect()
        @self.central_bindings.ee.on('disconnect')
        def on_disconnect():
            self.on_disconnect()
        @self.central_bindings.ee.on('rssi_update')
        def on_rssi_update():
            self.on_rssi_update()
        @self.central_bindings.ee.on('services_discover')
        def on_services_discover():
            self.on_services_discover()
        @self.central_bindings.ee.on('included_services_discover')
        def on_included_services_discover():
            self.on_included_services_discover()
        @self.central_bindings.ee.on('characteristics_discover')
        def on_characteristics_discover():
            self.on_characteristics_discover()

        @self.central_bindings.ee.on('read')
        def on_read():
            self.on_read()
        @self.central_bindings.ee.on('write')
        def on_write():
            self.on_write()
        @self.central_bindings.ee.on('broadcast')
        def on_broadcast():
            self.on_broadcast()
        @self.central_bindings.ee.on('notify')
        def on_notify():
            self.on_notify()
        @self.central_bindings.ee.on('descriptors_discover')
        def on_descriptors_discover():
            self.on_descriptors_discover()
        @self.central_bindings.ee.on('value_read')
        def on_value_read():
            self.on_value_read()
        @self.central_bindings.ee.on('value_write')
        def on_value_write():
            self.on_value_write()
        @self.central_bindings.ee.on('handle_read')
        def on_handle_read():
            self.on_handle_read()
        @self.central_bindings.ee.on('handle_write')
        def on_handle_write():
            self.on_handle_write()
        @self.central_bindings.ee.on('handle_notify')
        def on_handle_notify():
            self.on_handle_notify()
            

        @self.peripheral_bindings.ee.on('state_change')
        def on_peripheral_state_change(state):
            self.on_peripheral_state_change()
        @self.peripheral_bindings.ee.on('address_change')
        def on_peripheral_address_change(address):
            self.on_peripheral_address_change()
        # # @self...
