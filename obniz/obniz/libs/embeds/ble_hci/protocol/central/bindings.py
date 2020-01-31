from pyee import EventEmitter
from .gap import Gap

class NobleBindings:
    ee = EventEmitter()

    def __init__(self, hciProtocol):
        self._state = None

        self._addresses = {}
        self._addressTypes = {}
        self._connectable = {}

        self._pendingConnectionUuid = None
        self._connectionQueue = []

        self._handles = {}
        self._gatts = {}
        self._aclStream = None

        self._signalings = {}

        self._hci = hciProtocol
        self._gap = Gap(self._hci)

    def init(self):
        @self._gap.ee.on('scanStart')
        def onScanStart(filterDuplicates):
            self.onScanStart(filterDuplicates)
        @self._gap.ee.on('scanStop')
        def onScanStop():
            self.onScanStop()
        # @self._gap.ee.on('discover')
        # def onDiscover():
        #     self.onDiscover()

        @self._hci.ee.on('stateChange')
        def onStateChange(state):
            self.onStateChange(state)
        @self._hci.ee.on('addressChange')
        def onAddressChange(address):
            self.onAddressChange(address)
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
    
    def onStateChange(self, state):
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

        self.ee.emit('stateChange', state)

    def onAddressChange(self, address):
        self.ee.emit('addressChange', address)



    def onScanStart(self, filterDuplicates):
        self.ee.emit('scanStart', filterDuplicates)

    def onScanStop(self):
        self.ee.emit('scanStop')