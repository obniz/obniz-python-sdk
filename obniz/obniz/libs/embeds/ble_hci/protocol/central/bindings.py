from pyee import EventEmitter
from .gap import Gap

class NobleBindings:
    ee = EventEmitter()

    def __init__(self, hciProtocol):
        self._state = None

        self._addresses = {}
        self._address_types = {}
        self._connectable = {}

        self._pending_connection_uuid = None
        self._connection_queue = []

        self._handles = {}
        self._gatts = {}
        self._acl_stream = None

        self._signalings = {}

        self._hci = hciProtocol
        self._gap = Gap(self._hci)

    def start_scanning(self, service_uuids, allow_duplicates):
        self._scan_service_uuids = service_uuids or []
        
        self._gap.start_scanning(allow_duplicates)

    def stop_scanning(self):
        self._gap.stop_scanning()

    def init(self):
        @self._gap.ee.on('scan_start')
        def on_scan_start(filter_duplicates):
            self.on_scan_start(filter_duplicates)
        @self._gap.ee.on('scan_stop')
        def on_scan_top():
            self.on_scan_top()
        @self._gap.ee.on('discover')
        def on_discover(status, address, address_type, connectable, advertisement, rssi):
            self.on_discover(status, address, address_type, connectable, advertisement, rssi)
        @self._hci.ee.on('state_change')
        def on_state_change(state):
            self.on_state_change(state)
        @self._hci.ee.on('address_change')
        def on_address_change(address):
            self.on_address_change(address)
        # @self._hci.ee.on('leConnComplete')
        # def onLeConnComplete():
        #     self.onLeConnComplete()
        # @self._hci.ee.on('leConnUpdateComplete')
        # def onLeConnUpdateComplete():
        #     self.onLeConnUpdateComplete()
        # @self._hci.ee.on('rssiRead')
        # def onRssiRead():
        #     self.onRssiRead()
        # @self._hci.ee.on('disconnComplete')
        # def onDisconnComplete():
        #     self.onDisconnComplete()
        # @self._hci.ee.on('encryptChange')
        # def onEncryptChange():
        #     self.onEncryptChange()
    
    def on_state_change(self, state):
        if self._state == state:
            return
        self._state = state

        if state == 'unauthorized':
            print('noble warning: adapter state unauthorized, please run as root or with sudo')
            print('               or see README for information on running without root/sudo:')
            print('               https://github.com/sandeepmistry/noble#running-on-linux')
        elif state == 'unsupported':
            print('noble warning: adapter does not support Bluetooth Low Energy (BLE, Bluetooth Smart).')
            print('               Try to run with environment variable:')
            print('               [sudo] NOBLE_HCI_DEVICE_ID=x node ...')

        self.ee.emit('state_change', state)

    def on_address_change(self, address):
        self.ee.emit('address_change', address)

    def on_scan_start(self, filter_duplicates):
        self.ee.emit('scan_start', filter_duplicates)

    def on_scan_top(self):
        self.ee.emit('scan_stop')

    def on_discover(self, status, address, address_type, connectable, advertisement, rssi):

        try:
            self._scan_service_uuids
        except:
            return

        service_uuids = advertisement.service_uuids if "service_uuids" in advertisement else []
        service_data = advertisement.service_data if "service_data" in advertisement else []
        has_scan_service_uuids = len(self._scan_service_uuids) == 0

        if not has_scan_service_uuids:
            service_uuids = service_uuids[:]

        for i in service_data:
            service_uuids.append(service_data[i].uuid)

        for i in service_uuids:
            has_scan_service_uuids = service_uuids[i] in self._scan_service_uuids

            if has_scan_service_uuids:
                break

        if has_scan_service_uuids:
            uuid = ''.join(address.split(':'))
            self._addresses[uuid] = address
            self._address_types[uuid] = address_type
            self._connectable[uuid] = connectable

        self.ee.emit('discover', uuid, address, address_type, connectable, advertisement, rssi)
