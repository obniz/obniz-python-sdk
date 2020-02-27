from pyee import EventEmitter
from .gap import Gap
from .gatt import Gatt

class BlenoBindings:
    ee = EventEmitter()

    def __init__(self, hciProtocol):
        self._state = None

        self._advertising = False

        self._hci = hciProtocol
        self._gap = Gap(self._hci)
        # self._gatt = Gatt(self._hci)

        self._address = None
        self._handle = None
        self._acl_stream = None

    def init(self):
        @self._hci.ee.on('state_change')
        def on_state_change(state):
            self.on_state_change(state)

        @self._hci.ee.on('address_change')
        def on_address_change(address):
            self.on_address_change(address)

        @self._hci.ee.on('read_local_version')
        def onReadLocalVersion(hci_ver, hci_rev, lmp_ver, manufacturer, lmp_sub_ver):
            self.onReadLocalVersion(hci_ver, hci_rev, lmp_ver, manufacturer, lmp_sub_ver)

    def on_state_change(self, state):
        if self._state == state:
            return
        self._state = state

        if state == 'unauthorized':
            print('bleno warning: adapter state unauthorized, please run as root or with sudo')
            print('               or see README for information on running without root/sudo:')
            print('               https://github.com/sandeepmistry/bleno#running-on-linux')
        elif state == 'unsupported':
            print('bleno warning: adapter does not support Bluetooth Low Energy (BLE, Bluetooth Smart).')
            print('               Try to run with environment variable:')
            print('               [sudo] BLENO_HCI_DEVICE_ID=x node ...')

        self.ee.emit('state_change', state)

    def on_address_change(self, address):
        self.ee.emit('address_change', address)

    def onReadLocalVersion(self, hci_ver, hci_rev, lmp_ver, manufacturer, lmp_sub_ver):
        pass
