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
        self._aclStream = None

    def init(self):
        @self._hci.ee.on('stateChange')
        def onStateChange(state):
            self.onStateChange(state)

        @self._hci.ee.on('addressChange')
        def onAddressChange(address):
            self.onAddressChange(address)

        @self._hci.ee.on('readLocalVersion')
        def onReadLocalVersion(hciVer, hciRev, lmpVer, manufacturer, lmpSubVer):
            self.onReadLocalVersion(hciVer, hciRev, lmpVer, manufacturer, lmpSubVer)

    def onStateChange(self, state):
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

        self.ee.emit('stateChange', state)

    def onAddressChange(self, address):
        self.ee.emit('addressChange', address)

    def onReadLocalVersion(self, hciVer, hciRev, lmpVer, manufacturer, lmpSubVer):
        pass
