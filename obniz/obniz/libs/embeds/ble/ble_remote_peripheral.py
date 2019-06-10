import json

from pyee import AsyncIOEventEmitter

from .ble_helper import BleHelper
from .ble_remote_service import BleRemoteService


class BleRemotePeripheral:
    def __init__(self, obniz, address):
        self.obniz = obniz
        self.address = address
        self.connected = False

        self.device_type = None
        self.address_type = None
        self.ble_event_type = None
        self.rssi = None
        self.adv_data = None
        self.scan_resp = None

        self.keys = [
            "device_type",
            "address_type",
            "ble_event_type",
            "rssi",
            "adv_data",
            "scan_resp",
        ]

        self.services = []
        self.emitter = AsyncIOEventEmitter()

    def __str__(self):
        return json.dumps(
            {
                "address": self.address,
                "addressType": self.address_type,
                "advertisement": self.adv_data,
                "scanResponse": self.scan_resp,
                "rssi": self.rssi,
            },
            separators=(",", ":"),
            sort_keys=True,
        )

    def set_params(self, dic):
        self.advertise_data_rows = None
        for key in dic:
            if key in self.keys:
                setattr(self, key, dic[key])

        self.analyse_advertisement()

    def analyse_advertisement(self):
        if not self.advertise_data_rows:
            self.advertise_data_rows = []
            if self.adv_data:
                # print(f"self.adv_data: {self.adv_data}")
                # print(f"len(self.adv_data) : {len(self.adv_data)}")
                i = 0
                while i < len(self.adv_data):
                    # print(f"i: {i}")
                    length = self.adv_data[i]
                    # print(f"length: {length}")
                    arr = []
                    for j in range(0, length):
                        # print(f"j: {j}")
                        # print(f"i + j + 1: {i + j + 1}")
                        arr.append(self.adv_data[i + j + 1])
                        # print(f"self.adv_data[i + j + 1]: {self.adv_data[i + j + 1]}")

                    self.advertise_data_rows.append(arr)
                    i = i + length + 1

            if self.scan_resp:
                i = 0
                while i < len(self.scan_resp):
                    length = self.scan_resp[i]
                    arr = []
                    for j in range(0, length):
                        arr.append(self.scan_resp[i + j + 1])

                    self.advertise_data_rows.append(arr)
                    i = i + length + 1

            self.set_local_name()
            self.set_ibeacon()

    def search_type_val(self, type):
        self.analyse_advertisement()
        for row in self.advertise_data_rows:
            if row[0] == type:
                results = list(row)
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
            self.local_name = "".join([chr(i) for i in data])

    def set_ibeacon(self):
        data = self.search_type_val(0xFF)
        if (
            not data
            or data[0] != 0x4C
            or data[1] != 0x00
            or data[2] != 0x02
            or data[3] != 0x15
            or len(data) != 25
        ):
            self.ibeacon = None
            return

        uuid_data = data[4:20]
        uuid = ""
        for i in range(0, len(uuid_data)):
            uuid = uuid + format(uuid_data[i], "02x")
            if i == 4 - 1 or i == 4 + 2 - 1 or i == 4 + 2 * 2 - 1 or i == 4 + 2 * 3 - 1:
                uuid += "-"

        major = (data[20] << 8) + data[21]
        minor = (data[22] << 8) + data[23]
        power = data[24]

        self.ibeacon = {
            "uuid": uuid,
            "major": major,
            "minor": minor,
            "power": power,
            "rssi": self.rssi,
        }

    def _add_service_uuids(self, results, data, bit):
        if not data:
            return
        uuid_length = int(bit / 4)
        i = 0
        while i < len(data):
            end = i + uuid_length
            one = data[i:end]
            results.append(self.obniz.ble._data_array2uuid_hex(one, True))
            i = i + uuid_length

    def advertisement_service_uuids(self):
        results = []
        self._add_service_uuids(results, self.search_type_val(0x02), 16)
        self._add_service_uuids(results, self.search_type_val(0x03), 16)
        self._add_service_uuids(results, self.search_type_val(0x04), 32)
        self._add_service_uuids(results, self.search_type_val(0x05), 32)
        self._add_service_uuids(results, self.search_type_val(0x06), 64)
        self._add_service_uuids(results, self.search_type_val(0x07), 64)
        return results

    def connect(self):
        obj = {"ble": {"connect": {"address": self.address}}}
        self.obniz.send(obj)

    # connectWait() {
    #     return new Promise(resolve => {
    #         self.emitter.once('statusupdate', params => {
    #             resolve(params.status == 'connected')
    #         })
    #         self.connect()
    #     })
    # }

    def disconnect(self):
        obj = {"ble": {"disconnect": {"address": self.address}}}
        self.obniz.send(obj)

    # disconnectWait() {
    #     return new Promise(resolve => {
    #         self.emitter.once('statusupdate', params => {
    #             resolve(params.status == 'disconnected')
    #         })
    #         self.disconnect()
    #     })
    # }

    def get_service(self, uuid):
        uuid = BleHelper.uuid_filter(uuid)
        for service in self.services:
            if service.uuid == uuid:
                return service

        new_service = BleRemoteService({"uuid": uuid})
        new_service.parent = self
        self.services.append(new_service)
        return new_service

    def find_service(self, param):
        service_uuid = BleHelper.uuid_filter(param["service_uuid"])
        return self.get_service(service_uuid)

    def find_characteristic(self, param):
        service_uuid = BleHelper.uuid_filter(param["service_uuid"])
        characteristic_uuid = BleHelper.uuid_filter(param["characteristic_uuid"])
        s = self.get_service(service_uuid)
        if s:
            return s.get_characteristic(characteristic_uuid)

        return None

    def find_descriptor(self, param):
        descriptor_uuid = BleHelper.uuid_filter(param["descriptor_uuid"])
        c = self.find_characteristic(param)
        if c:
            return c.get_descriptor(descriptor_uuid)

        return None

    def discover_all_services(self):
        obj = {"ble": {"get_services": {"address": self.address}}}
        self.obniz.send(obj)

    # discoverAllServicesWait() {
    #     return new Promise(resolve => {
    #         self.emitter.once('discoverfinished', () => {
    #             children = self.services.filter(elm => {
    #                 return elm.discoverdOnRemote
    #             })
    #             resolve(children)
    #         })
    #         self.discoverAllServices()
    #     })
    # }

    # onconnect() {}

    def ondisconnect(self):
        pass

    def ondiscoverservice(self, child=None):
        pass

    def ondiscoverservicefinished(self):
        pass

    # ondiscover() {}

    # ondiscoverfinished() {}

    def notify_from_server(self, notify_name, params):
        self.emitter.emit(notify_name, params)
        if notify_name == "statusupdate":
            if params["status"] == "connected":
                self.connected = True
                self.onconnect()

            if params["status"] == "disconnected":
                self.connected = False
                self.ondisconnect()

        elif notify_name == "discover":
            child = self.get_service(params["service_uuid"])
            child.discoverdOnRemote = True
            self.ondiscoverservice(child)
        elif notify_name == "discoverfinished":
            children = [elm for elm in self.services if elm.discoverdOnRemote]
            self.ondiscoverservicefinished(children)

    def onerror(self):
        pass
