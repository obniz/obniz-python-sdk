import struct
from pyee import EventEmitter

HCI_COMMAND_PKT = 0x01
HCI_ACLDATA_PKT = 0x02
HCI_EVENT_PKT = 0x04

ACL_START_NO_FLUSH = 0x00
ACL_CONT = 0x01
ACL_START = 0x02

EVT_DISCONN_COMPLETE = 0x05
EVT_ENCRYPT_CHANGE = 0x08
EVT_CMD_COMPLETE = 0x0e
EVT_CMD_STATUS = 0x0f
EVT_NUMBER_OF_COMPLETED_PACKETS = 0x13
EVT_LE_META_EVENT = 0x3e

EVT_LE_CONN_COMPLETE = 0x01
EVT_LE_ADVERTISING_REPORT = 0x02
EVT_LE_CONN_UPDATE_COMPLETE = 0x03

OGF_LINK_CTL = 0x01
OCF_DISCONNECT = 0x0006

OGF_HOST_CTL = 0x03
OCF_SET_EVENT_MASK = 0x0001
OCF_RESET = 0x0003
OCF_READ_LE_HOST_SUPPORTED = 0x006c
OCF_WRITE_LE_HOST_SUPPORTED = 0x006d

OGF_INFO_PARAM = 0x04
OCF_READ_LOCAL_VERSION = 0x0001
OCF_READ_BUFFER_SIZE = 0x0005
OCF_READ_BD_ADDR = 0x0009

OGF_STATUS_PARAM = 0x05
OCF_READ_RSSI = 0x0005

OGF_LE_CTL = 0x08
OCF_LE_SET_EVENT_MASK = 0x0001
OCF_LE_READ_BUFFER_SIZE = 0x0002
OCF_LE_SET_ADVERTISING_PARAMETERS = 0x0006
OCF_LE_SET_ADVERTISING_DATA = 0x0008
OCF_LE_SET_SCAN_RESPONSE_DATA = 0x0009
OCF_LE_SET_ADVERTISE_ENABLE = 0x000a
OCF_LE_SET_SCAN_PARAMETERS = 0x000b
OCF_LE_SET_SCAN_ENABLE = 0x000c
OCF_LE_CREATE_CONN = 0x000d
OCF_LE_CONN_UPDATE = 0x0013
OCF_LE_START_ENCRYPTION = 0x0019
OCF_LE_LTK_NEG_REPLY = 0x001b

DISCONNECT_CMD = OCF_DISCONNECT | (OGF_LINK_CTL << 10)

SET_EVENT_MASK_CMD = OCF_SET_EVENT_MASK | (OGF_HOST_CTL << 10)
RESET_CMD = OCF_RESET | (OGF_HOST_CTL << 10)
READ_LE_HOST_SUPPORTED_CMD = OCF_READ_LE_HOST_SUPPORTED | (OGF_HOST_CTL << 10)
WRITE_LE_HOST_SUPPORTED_CMD = OCF_WRITE_LE_HOST_SUPPORTED | (OGF_HOST_CTL << 10)

READ_LOCAL_VERSION_CMD = OCF_READ_LOCAL_VERSION | (OGF_INFO_PARAM << 10)
READ_BUFFER_SIZE_CMD = OCF_READ_BUFFER_SIZE | (OGF_INFO_PARAM << 10)
READ_BD_ADDR_CMD = OCF_READ_BD_ADDR | (OGF_INFO_PARAM << 10)

READ_RSSI_CMD = OCF_READ_RSSI | (OGF_STATUS_PARAM << 10)

LE_SET_EVENT_MASK_CMD = OCF_LE_SET_EVENT_MASK | (OGF_LE_CTL << 10)
LE_READ_BUFFER_SIZE_CMD = OCF_LE_READ_BUFFER_SIZE | (OGF_LE_CTL << 10)
LE_SET_SCAN_PARAMETERS_CMD = OCF_LE_SET_SCAN_PARAMETERS | (OGF_LE_CTL << 10)
LE_SET_SCAN_ENABLE_CMD = OCF_LE_SET_SCAN_ENABLE | (OGF_LE_CTL << 10)
LE_CREATE_CONN_CMD = OCF_LE_CREATE_CONN | (OGF_LE_CTL << 10)
LE_CONN_UPDATE_CMD = OCF_LE_CONN_UPDATE | (OGF_LE_CTL << 10)
LE_START_ENCRYPTION_CMD = OCF_LE_START_ENCRYPTION | (OGF_LE_CTL << 10)
LE_SET_ADVERTISING_PARAMETERS_CMD = OCF_LE_SET_ADVERTISING_PARAMETERS | (OGF_LE_CTL << 10)

LE_SET_ADVERTISING_DATA_CMD = OCF_LE_SET_ADVERTISING_DATA | (OGF_LE_CTL << 10)
LE_SET_SCAN_RESPONSE_DATA_CMD = OCF_LE_SET_SCAN_RESPONSE_DATA | (OGF_LE_CTL << 10)
LE_SET_ADVERTISE_ENABLE_CMD = OCF_LE_SET_ADVERTISE_ENABLE | (OGF_LE_CTL << 10)
LE_LTK_NEG_REPLY_CMD = OCF_LE_LTK_NEG_REPLY | (OGF_LE_CTL << 10)

HCI_OE_USER_ENDED_CONNECTION = 0x13


class Hci:
    ee = EventEmitter()

    class Socket:
        def __init__(self, obnizHci):
            self._obnizHci = obnizHci

        def write(self, data):
            arr = list(data)
            self._obnizHci.write(arr)

    def onSocketData(self, array):
        data = list(array)
        # debug('onSocketData: ' + data.toString('hex'))

        eventType = data[0]
        # debug('\tevent type = ' + eventType);

        if HCI_EVENT_PKT == eventType:
            subEventType = data[1]

            # debug('\tsub event type = ' + subEventType)

            if subEventType == EVT_DISCONN_COMPLETE:
                print("wip")
            elif subEventType == EVT_ENCRYPT_CHANGE:
                print("wip")
            elif subEventType == EVT_CMD_COMPLETE:
                ncmd = data[3]
                cmd = struct.unpack("<h", bytearray(data[4:6]))[0]
                status = data[6]
                result = data[7:]

                # debug('\t\tncmd = ' + ncmd);
                # debug('\t\tcmd = ' + cmd);
                # debug('\t\tstatus = ' + status);
                # debug('\t\tresult = ' + result.toString('hex'));

                self.processCmdCompleteEvent(cmd, status, result)
            elif subEventType == EVT_CMD_STATUS:
                print("wip")
            elif subEventType == EVT_LE_META_EVENT:
                print("wip")
            elif subEventType == EVT_NUMBER_OF_COMPLETED_PACKETS:
                print("wip")
        elif HCI_ACLDATA_PKT == eventType:
            print("wip")
        elif HCI_COMMAND_PKT == eventType:
            print("wip")

    def __init__(self, obnizHci):
        self._obnizHci = obnizHci
        self._state = None

        self._handleBuffers = {}

        self._socket = self.Socket(self._obnizHci)

        self._obnizHci.onread = self.onSocketData

    # util.inherits(Hci, events.EventEmitter)

    # Hci.STATUS_MAPPER = STATUS_MAPPER

    async def init_wait(self):
        self.reset()
        # // this.setEventMask();
        # // this.setLeEventMask();
        # // this.readLocalVersion();
        # // this.writeLeHostSupported();
        # // this.readLeHostSupported();
        # // this.readBdAddr();

        # return new Promise(resolve => {
        #     this.once('stateChange', () => {
        #     // console.log('te');
        #     resolve();
        #     });
        # });

    def setEventMask(self):
        cmd = bytearray([0x00]*12)
        eventMask = list(bytes.fromhex('fffffbff07f8bf3d'))

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", SET_EVENT_MASK_CMD)

        # # length
        cmd[3] = len(eventMask)

        eventMask[4:8] = cmd[:]

        # # debug('set event mask - writing: ' + cmd.toString('hex'))
        self._socket.write(cmd)

    def reset(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (OCF_RESET | (OGF_HOST_CTL << 10)))

        # length
        cmd[3] = 0x00

        # debug('reset - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    def resetBuffers(self):
        self._handleAclsInProgress = {}
        self._handleBuffers = {}
        self._aclOutQueue = []

    def readLocalVersion(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_LOCAL_VERSION_CMD))

        # length
        cmd[3] = 0x00

        # debug('read local version - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    def readBdAddr(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_BD_ADDR_CMD))

        # length
        cmd[3] = 0x00

        # debug('read bd addr - writing: ' + cmd.toString('hex'))
        self._socket.write(cmd)

    def setLeEventMask(self):
        cmd = bytearray([0x00]*4)
        leEventMask = list(bytes.fromhex('1f00000000000000'))

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (LE_SET_EVENT_MASK_CMD))

        # length
        cmd[3] = 0x00

        leEventMask[4:8] = cmd[:]

        # # debug('set le event mask - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    def readLeHostSupported(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_LE_HOST_SUPPORTED_CMD))

        # length
        cmd[3] = 0x00

        # debug('read LE host supported - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    def writeLeHostSupported(self):
        cmd = bytearray([0x00]*6)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (WRITE_LE_HOST_SUPPORTED_CMD))

        # length
        cmd[3] = 0x02

        # data
        cmd[4] = 0x01
        cmd[5] = 0x00

        # debug('write LE host supported - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    def setScanParameters(self):
        cmd = bytearray([0x00]*11)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (LE_SET_SCAN_PARAMETERS_CMD))

        # length
        cmd[3] = 0x07

        # data
        cmd[4] = 0x01
        cmd[5:7] = struct.pack("<h", 0x0010)
        cmd[7:9] = struct.pack("<h", 0x0010)
        cmd[9] = 0x00
        cmd[10] = 0x00

        # debug('set scan parameters - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    def setScanEnabled(self, enabled, filterDuplicates):
        cmd = bytearray([0x00]*6)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (LE_SET_SCAN_ENABLE_CMD))

        # length
        cmd[3] = 0x02

        # data
        cmd[4] =  0x01 if enabled else 0x00
        cmd[5] =  0x01 if filterDuplicates else 0x00

        # debug('set scan enabled - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    ## def...

    def leReadBufferSize(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (LE_READ_BUFFER_SIZE_CMD))

        # length
        cmd[3] = 0x00

        # debug('le read buffer size - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    def readBufferSize(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_BUFFER_SIZE_CMD))

        # length
        cmd[3] = 0x0

        # debug('read buffer size - writing: ' + cmd.toString('hex'));
        self._socket.write(cmd)

    ## def...

    def processCmdCompleteEvent(self, cmd, status, result):
        if cmd == RESET_CMD:
            self.resetBuffers()
            self.setEventMask()
            self.setLeEventMask()
            self.readLocalVersion()
            self.readBdAddr()
            self.writeLeHostSupported()
            self.readLeHostSupported()
            self.leReadBufferSize()

        elif cmd == READ_LE_HOST_SUPPORTED_CMD:
            if status == 0:
                le = result[0]
                simul = result[1]

                # debug('\t\t\tle = ' + le)
                # debug('\t\t\tsimul = ' + simul)

        elif cmd == READ_LOCAL_VERSION_CMD:
            hciVer = result[0]
            hciRev = struct.unpack("<h", bytearray(result[1:3]))[0]
            lmpVer = result[3]
            manufacturer = struct.unpack("<h", bytearray(result[4:6]))[0]
            lmpSubVer = struct.unpack("<h", bytearray(result[6:8]))[0]

            if hciVer < 0x06:
                self.ee.emit("stateChange", self, "unsuported")
            elif not self._state == "poweredOn":
                self.setScanEnabled(False, True)
                self.setScanParameters()
            
            # self.ee.emit('readLocalVersion',
            #     hciVer,
            #     hciRev,
            #     lmpSubVer,
            #     manufacturer,
            #     lmpSubVer
            # ) 
            # # -> BlenoBindings

        elif cmd == READ_BD_ADDR_CMD:
            self.addressType = 'public'
            self.address = ':'.join([format(r, 'x') for r in reversed(result)])

            # debug('address = ' + this.address)

            # self.ee.emit('addressChange', self.address)

        elif cmd == LE_SET_SCAN_PARAMETERS_CMD:
            # self.ee.emit('stateChange', 'poweredOn')

            # self.ee.emit('leScanParametersSet')
            pass

        elif cmd == LE_SET_SCAN_ENABLE_CMD:
            # self.ee.emit('leScanEnableSet', status)
            pass

        elif cmd == LE_SET_ADVERTISING_PARAMETERS_CMD:
            print("wip: LE_SET_ADVERTISING_PARAMETERS_CMD")

        elif cmd == LE_SET_ADVERTISING_DATA_CMD:
            print("wip: LE_SET_ADVERTISING_DATA_CMD")

        elif cmd == LE_SET_SCAN_RESPONSE_DATA_CMD:
            print("wip: LE_SET_SCAN_RESPONSE_DATA_CMD")

        elif cmd == LE_SET_ADVERTISE_ENABLE_CMD:
            print("wip: LE_SET_ADVERTISE_ENABLE_CMD")

        elif cmd == READ_RSSI_CMD:
            print("wip: READ_RSSI_CMD")

        elif cmd == LE_LTK_NEG_REPLY_CMD:
            print("wip: LE_LTK_NEG_REPLY_CMD")

        elif cmd == LE_READ_BUFFER_SIZE_CMD:
            if not status:
                self.processLeReadBufferSize(result)

        elif cmd == READ_BUFFER_SIZE_CMD:
            print("wip: READ_BUFFER_SIZE_CMD")

    # def...

    def processLeReadBufferSize(self, result):
        aclMtu = struct.unpack("<h", bytearray(result[0:2]))[0]
        aclMaxInProgress = result[2]
        if not aclMtu:
            # // as per Bluetooth specs
            # debug('falling back to br/edr buffer size');
            self.readBufferSize()
        else:
            # debug('le acl mtu = ' + aclMtu);
            # debug('le acl max in progress = ' + aclMaxInProgress);
            self._aclMtu = aclMtu
            self._aclMaxInProgress = aclMaxInProgress

    @ee.on('stateChange')
    def onStateChange(self, state):
        self._state = state
