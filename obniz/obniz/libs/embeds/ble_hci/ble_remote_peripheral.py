from pyee import EventEmitter
from .ble_remote_service import BleRemoteService
from .ble_helper import BleHelper

class BleRemotePeripheral:
    ee = EventEmitter()
    def __init__(self, obnizBle, address):
        self.obnizBle = obnizBle
        self.address = address
        self.connected = False

        self.device_type = None
        self.address_type = None
        self.ble_event_type = None
        self.rssi = None
        self.adv_data = None
        self.scan_resp = None

        self.keys = [
            'device_type',
            'address_type',
            'ble_event_type',
            'rssi',
            'adv_data',
            'scan_resp',
        ]

        self.services = []

    ## def...

    def set_params(self, dic):
        self.advertise_data_rows = None
        for key in dic:
            if key in dic and key in self.keys:
                if type(dic[key]) is str:
                    exec('self.{} = "{}"'.format(key, dic[key]))
                else:
                    exec('self.{} = {}'.format(key, dic[key]))
        self.analyse_advertisement()
    
    def analyse_advertisement(self):
        if not self.advertise_data_rows:
            self.advertise_data_rows = []
            if self.adv_data:
                i = 0
                while ( i < len(self.adv_data)):
                    length = self.adv_data[i]
                    arr = [0] * length
                    for j in range(length):
                        arr[j] = self.adv_data[i + j + 1]
                    self.advertise_data_rows.append(arr)
                    i += length
                    i += 1
            if self.scan_resp:
                i = 0
                while (i < len(self.scan_resp)):
                    length = self.scan_resp[i]
                    arr = [0] * length
                    for j in range(length):
                        arr[j] = self.scan_resp[i + j + 1]
                    self.advertise_data_rows.append(arr)
                    i += length
                    i += 1
            self.set_local_name()
            self.set_i_beacon()

    def search_type_val(self, typ):
        self.analyse_advertisement()
        for advertise_data_row in self.advertise_data_rows:
            if advertise_data_row[0] is typ:
                results = advertise_data_row[:]
                results.pop(0)
                return results
        return None

    def set_local_name(self):
        data = self.search_type_val(0x09)
        if not data:
            data = self.search_type_val(0x08)
        if not data:
            self.local_name = None
        else:
            self.local_name = ''.join(map(chr, data))

    def set_i_beacon(self):
        data = self.search_type_val(0xff)
        if (not data 
            or data[0] is not 0x4c 
            or data[1] is not 0x00 
            or data[2] is not 0x02 
            or data[3] is not 0x15 
            or len(data) is not 25):
            self.i_bracon = None
            return

        uuid_data = data[4:20]
        uuid = ''
        for i in range(len(uuid_data)):
            uuid += format(uuid_data[i], '02x')[-2:]
            if (i is 4 - 1 
                or i is 4 + 2 - 1 
                or i is 4 + 2 * 2 - 1 
                or i is 4 + 2 * 3 - 1):
                uuid += '_'
        major = (data[20] << 8) + data[21]
        minor = (data[22] << 8) + data[23]
        power = data[24]

        self.i_beacon = {
            "uuid": uuid,
            "major": major,
            "minor": minor,
            "power": power,
            "rssi": self.rssi,
        }

