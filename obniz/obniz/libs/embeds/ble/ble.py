from .ble_advertisement import BleAdvertisement
from .ble_characteristic import BleCharacteristic
from .ble_descriptor import BleDescriptor
from .ble_peripheral import BlePeripheral
from .ble_remote_peripheral import BleRemotePeripheral
from .ble_scan import BleScan
from .ble_service import BleService


class ObnizBLE:
    def __init__(self, obniz):
        self.obniz = obniz
        self.remote_peripherals = []

        self.service = BleService
        self.characteristic = BleCharacteristic
        self.descriptor = BleDescriptor
        self.peripheral = BlePeripheral(obniz)

        self.scanTarget = None

        self.advertisement = BleAdvertisement(obniz)
        self.scan = BleScan(obniz)
        self._reset()

    def _reset(self):
        pass

    def find_peripheral(self, address):
        for remote_peripheral in self.remote_peripherals:
            if remote_peripheral.address == address:
                return remote_peripheral

        return None

    def notified(self, obj):
        if "scan_result" in obj:
            val = self.find_peripheral(obj["scan_result"]["address"])
            if not val:
                val = BleRemotePeripheral(self.obniz, obj["scan_result"]["address"])
                self.remote_peripherals.append(val)

            val.discoverdOnRemote = True
            val.set_params(obj["scan_result"])

            self.scan.notify_from_server("onfind", val)

        if "scan_result_finish" in obj:
            self.scan.notify_from_server("onfinish")

        def remote_peripheral_callback_func(val, func, type):
            obj = None
            if val is None:
                return
            p = self.find_peripheral(val["address"])
            if not p:
                return

            if type == "peripheral":
                obj = p
            elif type == "service":
                obj = p.find_service(val)
            elif type == "characteristic":
                obj = p.find_characteristic(val)
            elif type == "descriptor":
                obj = p.find_descriptor(val)

            if not obj:
                return

            func(val, obj)

        param_list = {
            "status_update": {"name": "statusupdate", "obj": "peripheral"},
            "get_service_result": {"name": "discover", "obj": "peripheral"},
            "get_service_result_finish": {
                "name": "discoverfinished",
                "obj": "peripheral",
            },
            "get_characteristic_result": {"name": "discover", "obj": "service"},
            "get_characteristic_result_finish": {
                "name": "discoverfinished",
                "obj": "service",
            },
            "write_characteristic_result": {"name": "onwrite", "obj": "characteristic"},
            "read_characteristic_result": {"name": "onread", "obj": "characteristic"},
            "register_notify_characteristic_result": {
                "name": "onregisternotify",
                "obj": "characteristic",
            },
            "unregister_notify_characteristic_result": {
                "name": "onunregisternotify",
                "obj": "characteristic",
            },
            "nofity_characteristic": {"name": "onnotify", "obj": "characteristic"},
            "get_descriptor_result": {"name": "discover", "obj": "characteristic"},
            "get_descriptor_result_finish": {
                "name": "discoverfinished",
                "obj": "characteristic",
            },
            "write_descriptor_result": {"name": "onwrite", "obj": "descriptor"},
            "read_descriptor_result": {"name": "onread", "obj": "descriptor"},
        }

        for key in param_list:
            remote_peripheral_callback_func(
                obj.get(key),
                lambda val, bleobj: bleobj.notify_from_server(
                    param_list[key]["name"], val
                ),
                param_list[key]["obj"],
            )

        def callback_func(val, func, type):
            obj = None
            if val is None:
                return
            if type == "peripheral":
                obj = self.peripheral
            elif type == "service":
                obj = self.peripheral.get_service(val)
            elif type == "characteristic":
                obj = self.peripheral.find_characteristic(val)
            elif type == "descriptor":
                obj = self.peripheral.find_descriptor(val)

            if not obj:
                return

            func(val, obj)

        if "peripheral" in obj:
            callback_func(
                obj["peripheral"].get("connection_status"),
                lambda val, _bleobj: self.peripheral.onconnectionupdates(val),
                "peripheral",
            )

            param_list = {
                "read_characteristic_result": {
                    "name": "onread",
                    "obj": "characteristic",
                },
                "write_characteristic_result": {
                    "name": "onwrite",
                    "obj": "characteristic",
                },
                "notify_read_characteristic": {
                    "name": "onreadfromremote",
                    "obj": "characteristic",
                },
                "notify_write_characteristic": {
                    "name": "onwritefromremote",
                    "obj": "characteristic",
                },
                "read_descriptor_result": {"name": "onread", "obj": "descriptor"},
                "write_descriptor_result": {"name": "onwrite", "obj": "descriptor"},
                "notify_read_descriptor": {
                    "name": "onreadfromremote",
                    "obj": "descriptor",
                },
                "notify_write_descriptor": {
                    "name": "onwritefromremote",
                    "obj": "descriptor",
                },
            }

            for key in param_list:
                callback_func(
                    obj["peripheral"].get(key),
                    lambda val, bleobj: bleobj.notify_from_server(
                        param_list[key]["name"], val
                    ),
                    param_list[key]["obj"],
                )

        if "error" in obj:
            params = obj["error"]
            handled = False
            if not params["address"]:
                peripheral = self.peripheral
            else:
                peripheral = self.find_peripheral(params["address"])

            if peripheral:
                if (
                    "service_uuid" in params
                    and "characteristic_uuid" in params
                    and "descriptor_uuid" in params
                ):
                    target = peripheral.find_descriptor(params)
                elif "service_uuid" in params and "characteristic_uuid" in params:
                    target = peripheral.find_characteristic(params)
                elif "service_uuid" in params:
                    target = peripheral.find_service(params)

                if target:
                    target.notify_from_server("onerror", params)
                    handled = True
                else:
                    peripheral.onerror(params)
                    handled = True

            if not handled:
                self.obniz.error(
                    "ble "
                    + params["message"]
                    + " service="
                    + params["service_uuid"]
                    + " "
                    + "characteristic_uuid="
                    + params["characteristic_uuid"]
                    + " "
                    + "descriptor_uuid="
                    + params["descriptor_uuid"]
                )

    @classmethod
    def _data_array2uuid_hex(cls, data, reverse):
        uuid = []
        for d in data:
            uuid.append(format(d, "02x"))

        if reverse:
            uuid.reverse()

        str = "".join(uuid)
        if len(uuid) >= 16:
            str = (
                str[0:8]
                + "-"
                + str[8:12]
                + "-"
                + str[12:16]
                + "-"
                + str[16:20]
                + "-"
                + str[20:]
            )

        return str
