import struct
from pyee import EventEmitter
import asyncio
import re

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

# let STATUS_MAPPER = require('./hci-status')


class Hci:
    ee = EventEmitter()

    class Socket:
        def __init__(self, obnizHci):
            self._obnizHci = obnizHci

        def write(self, data):
            arr = list(data)
            self._obnizHci.write(arr)

    def on_socket_data(self, array):
        data = list(array)
        event_type = data[0]

        if HCI_EVENT_PKT == event_type:
            sub_event_type = data[1]

            if sub_event_type == EVT_DISCONN_COMPLETE:
                print("wip: EVT_DISCONN_COMPLETE")
            elif sub_event_type == EVT_ENCRYPT_CHANGE:
                print("wip: EVT_ENCRYPT_CHANGE")
            elif sub_event_type == EVT_CMD_COMPLETE:
                ncmd = data[3]
                cmd = struct.unpack("<h", bytearray(data[4:6]))[0]
                status = data[6]
                result = data[7:]

                self.process_cmd_complete_event(cmd, status, result)
            elif sub_event_type == EVT_CMD_STATUS:
                print("wip: EVT_CMD_STATUS")
            elif sub_event_type == EVT_LE_META_EVENT:
                le_meta_event_type = data[3]
                le_meta_event_status = data[4]
                le_meta_event_data = data[5:]

                self.process_le_meta_event(
                    le_meta_event_type, le_meta_event_status, le_meta_event_data)
            elif sub_event_type == EVT_NUMBER_OF_COMPLETED_PACKETS:
                print("wip: EVT_NUMBER_OF_COMPLETED_PACKETS:", EVT_NUMBER_OF_COMPLETED_PACKETS)
                handles = data[3]
                for i in range(handles):
                    handle = struct.unpack("<h", bytearray(data[4+i*4:4+i*4+2]))[0]
                    pkts = struct.unpack("<h", bytearray(data[6+i*4:6+i*4+2]))[0]
                    if len(self._handle_acls_in_progress) < handle:
                        continue
                    if pkts > self._handle_acls_in_progress[handle]:
                        self._handle_acls_in_progress[handle] = 0
                    else:
                        self._handle_acls_in_progress[handle] -= pkts
                self.push_acl_out_queue()

        elif HCI_ACLDATA_PKT == event_type:
            print("wip")
        elif HCI_COMMAND_PKT == event_type:
            print("wip")

    def __init__(self, obnizHci):
        self.observers = []
        self._obnizHci = obnizHci
        self._state = None

        self._handle_buffers = {}

        @self.ee.on('state_change')
        def on_state_change(state):
            self.on_state_change(state)

        self._socket = self.Socket(self._obnizHci)

        self._obnizHci.onread = self.on_socket_data

    # util.inherits(Hci, events.EventEmitter)

    # Hci.STATUS_MAPPER = STATUS_MAPPER

    def init_wait(self):
        self.reset()
        # // this.set_event_mask();
        # // this.set_le_event_mask();
        # // this.read_local_version();
        # // this.write_le_host_supported();
        # // this.read_le_host_supported();
        # // this.read_bd_addr();

        future = asyncio.get_event_loop().create_future()

        @self.ee.once('state_change')
        def on_state_change(state):
            future.set_result(state)
            # print('te')

        return future

    def set_event_mask(self):
        cmd = bytearray([0x00]*12)
        event_Mask = list(bytes.fromhex('fffffbff07f8bf3d'))

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", SET_EVENT_MASK_CMD)

        # # length
        cmd[3] = len(event_Mask)

        cmd[4:12] = event_Mask

        self._socket.write(cmd)

    def reset(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (OCF_RESET | (OGF_HOST_CTL << 10)))

        # length
        cmd[3] = 0x00

        self._socket.write(cmd)

    def reset_buffers(self):
        self._handle_acls_in_progress = {}
        self._handle_buffers = {}
        self._acl_out_queue = []

    def read_local_version(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_LOCAL_VERSION_CMD))

        # length
        cmd[3] = 0x00

        self._socket.write(cmd)

    def read_bd_addr(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_BD_ADDR_CMD))

        # length
        cmd[3] = 0x00

        self._socket.write(cmd)

    def set_le_event_mask(self):
        cmd = bytearray([0x00]*4)
        le_event_mask = list(bytes.fromhex('1f00000000000000'))

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (LE_SET_EVENT_MASK_CMD))

        # length
        cmd[3] = len(le_event_mask)

        cmd[4:12] = le_event_mask
        self._socket.write(cmd)

    def read_le_host_supported(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_LE_HOST_SUPPORTED_CMD))

        # length
        cmd[3] = 0x00

        self._socket.write(cmd)

    def write_le_host_supported(self):
        cmd = bytearray([0x00]*6)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (WRITE_LE_HOST_SUPPORTED_CMD))

        # length
        cmd[3] = 0x02

        # data
        cmd[4] = 0x01
        cmd[5] = 0x00

        self._socket.write(cmd)

    def set_scan_parameters(self):
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

        self._socket.write(cmd)

    def set_scan_enabled(self, enabled, filter_duplicates):
        cmd = bytearray([0x00]*6)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (LE_SET_SCAN_ENABLE_CMD))

        # length
        cmd[3] = 0x02

        # data
        cmd[4] = 0x01 if enabled else 0x00
        cmd[5] = 0x01 if filter_duplicates else 0x00

        self._socket.write(cmd)

    # def...

    def le_read_buffer_size(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (LE_READ_BUFFER_SIZE_CMD))

        # length
        cmd[3] = 0x00

        self._socket.write(cmd)

    def read_buffer_size(self):
        cmd = bytearray([0x00]*4)

        # header
        cmd[0] = HCI_COMMAND_PKT
        cmd[1:3] = struct.pack("<h", (READ_BUFFER_SIZE_CMD))

        # length
        cmd[3] = 0x0

        self._socket.write(cmd)

    # def...

    def push_acl_out_queue(self):
        in_progress = 0
        for handle in self._handle_acls_in_progress:
            in_progress += self._handle_acls_in_progress[handle]
        while in_progress < self._acl_max_in_progress and len(self._acl_out_queue):
            in_progress += 1
            self.write_one_acl_data_pkt()

        if in_progress >= self._acl_max_in_progress and len(self._acl_out_queue):
            pass

    def write_one_acl_data_pkt(self):
        pkt = self._acl_out_queue.pop()
        self._handle_acls_in_progress[pkt.handle] += 1

        self._socket.write(pkt.pkt)

    # def...

    def process_cmd_complete_event(self, cmd, status, result):
        if cmd == RESET_CMD:
            self.reset_buffers()
            self.set_event_mask()
            self.set_le_event_mask()
            self.read_local_version()
            self.read_bd_addr()
            self.write_le_host_supported()
            self.read_le_host_supported()
            self.le_read_buffer_size()

        elif cmd == READ_LE_HOST_SUPPORTED_CMD:
            if status == 0:
                le = result[0]
                simul = result[1]

        elif cmd == READ_LOCAL_VERSION_CMD:
            hci_ver = result[0]
            hci_rev = struct.unpack("<h", bytearray(result[1:3]))[0]
            lmp_ver = result[3]
            manufacturer = struct.unpack("<h", bytearray(result[4:6]))[0]
            lmp_sub_ver = struct.unpack("<h", bytearray(result[6:8]))[0]

            if hci_ver < 0x06:
                self.ee.emit("state_change", "unsupported")
            elif not self._state == "poweredOn":
                self.set_scan_enabled(False, True)
                self.set_scan_parameters()

            self.ee.emit('read_local_version',
                         hci_ver,
                         hci_rev,
                         lmp_ver,
                         manufacturer,
                         lmp_sub_ver
                         )

        elif cmd == READ_BD_ADDR_CMD:
            self.addressType = 'public'
            self.address = ':'.join([format(r, 'x') for r in reversed(result)])

            self.ee.emit('address_change', self.address)

        elif cmd == LE_SET_SCAN_PARAMETERS_CMD:
            self.ee.emit('state_change', 'poweredOn')

            self.ee.emit('le_scan_parameters_set')

        elif cmd == LE_SET_SCAN_ENABLE_CMD:
            self.ee.emit('le_scan_enable_set', status)

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
                self.process_le_read_buffer_size(result)

        elif cmd == READ_BUFFER_SIZE_CMD:
            print("wip: READ_BUFFER_SIZE_CMD")

    def process_le_meta_event(self, event_type, status, data):
        if event_type == EVT_LE_CONN_COMPLETE:
            self.process_le_conn_complete(status, data)
        elif event_type == EVT_LE_ADVERTISING_REPORT:
            self.process_le_advertising_report(status, data)
        elif event_type == EVT_LE_CONN_UPDATE_COMPLETE:
            self.process_le_conn_update_complete(status, data)

    def process_le_conn_complete(self, status, data):
        print("wip: EVT_LE_CONN_COMPLETE")

    def process_le_advertising_report(self, count, data):
        for i in range(count):
            typ = data[0]
            address_type = 'random' if data[1] == 0x01 else 'public'
            address = ":".join(reversed([re.match('.{1,2}', str(format(x, '02x'))).group()
                      for x in data[2:8]]))

            eir_length = data[8]
            eir = data[9: eir_length + 9]
            rssi = data[eir_length + 9]

            self.ee.emit("le_advertising_report", 0, typ, address, address_type, eir, rssi)

            data = data[eir_length + 10:]



    def process_le_conn_update_complete(self, status, data):
        print("wip: EVT_LE_CONN_UPDATE_COMPLETE")

    # def...

    def process_le_read_buffer_size(self, result):
        acl_mtu = struct.unpack("<h", bytearray(result[0:2]))[0]
        acl_max_in_progress = result[2]
        if not acl_mtu:
            # // as per Bluetooth specs
            self.read_buffer_size()
        else:
            self._acl_mtu = acl_mtu
            self._acl_max_in_progress = acl_max_in_progress

    def on_state_change(self, state):
        self._state = state
