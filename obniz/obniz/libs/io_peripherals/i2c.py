from ..utils.util import ObnizUtil

import asyncio

class PeripheralI2C:
    def __init__(self, obniz, id):
        self.obniz = obniz
        self.id = id
        self._reset()

    def _reset(self):
        self.observers = []
        self.state = {}
        self.used = False
        self.onwritten = None

    def add_observer(self, callback):
        if callback:
            self.observers.append(callback)

    def start(self, arg):
        err = ObnizUtil._required_keys(arg, ["mode", "sda", "scl"])
        if err:
            raise Exception("I2C start param '" + err + "' required, but not found ")

        self.state = ObnizUtil._key_filter(arg, ["mode", "sda", "scl", "pull", "gnd"])

        io_keys = ["sda", "scl", "gnd"]
        for key in io_keys:
            if key in self.state and not self.obniz.is_valid_io(self.state[key]):
                raise Exception("i2c start param '" + key + "' are to be valid io no")

        mode = self.state["mode"]
        if type(arg.get("clock")) is int:
            clock = int(arg["clock"])
        else:
            clock = None
        if type(arg.get("slave_address")) is int:
            slave_address = int(arg["slave_address"])
        else:
            slave_address = None

        if type(arg.get("slave_address_length")) is int:
            slave_address_length = int(arg["slave_address_length"])
        else:
            slave_address_length = None

        if mode != "master" and mode != "slave":
            raise Exception("i2c: invalid mode " + mode)

        if mode == "master":
            if clock is None:
                raise Exception("i2c: please specify clock when master mode")

            if clock <= 0 or clock > 1 * 1000 * 1000:
                raise Exception("i2c: invalid clock " + clock)

            if arg["pull"] == "5v" and clock > 400 * 1000:
                raise Exception(
                    "i2c: please use under 400khz when internal 5v internal pull-up"
                )

            if arg["pull"] == "3v" and clock > 100 * 1000:
                raise Exception(
                    "i2c: please use under 100khz when internal 3v internal pull-up"
                )

        else:
            if slave_address is None:
                raise Exception("i2c: please specify slave_address")

            if slave_address < 0 or slave_address > 0x7F:
                raise Exception("i2c: invalid slave_address")

            if slave_address < 0 or slave_address > 0x7F:
                raise Exception("i2c: invalid slave_address")

            if slave_address_length is not None and slave_address_length != 7:
                raise Exception("i2c: invalid slave_address_length. please specify 7")

        self.obniz.get_io(self.state["sda"]).drive("open-drain")
        self.obniz.get_io(self.state["scl"]).drive("open-drain")

        if "pull" in self.state:
            self.obniz.get_io(self.state["sda"]).pull(self.state["pull"])
            self.obniz.get_io(self.state["scl"]).pull(self.state["pull"])
        else:
            self.obniz.get_io(self.state["sda"]).pull(None)
            self.obniz.get_io(self.state["scl"]).pull(None)

        if "gnd" in self.state:
            self.obniz.get_io(self.state["gnd"]).output(False)
            # ioNames = {}
            # ioNames[self.state["gnd"]] = 'gnd'
            # self.obniz.display.setPinNames('i2c' + str(self.id), ioNames)

        start_obj = ObnizUtil._key_filter(self.state, ["mode", "sda", "scl"])
        if mode == "master":
            start_obj["clock"] = clock
        else:
            start_obj["slave_address"] = slave_address
            if slave_address_length:
                start_obj["slave_address_length"] = slave_address_length

        obj = {}
        obj["i2c" + str(self.id)] = start_obj
        self.used = True
        self.obniz.send(obj)

    def write(self, address, data):
        if not self.used:
            raise Exception("i2c{} is not started".format(self.id))

        address = int(address)
        if not address:
            raise Exception("i2c: please specify address")

        if address < 0 or address > 0x7F:
            raise Exception("i2c: invalid address")

        if not data:
            raise Exception("i2c: please provide data")

        if len(data) > 1024:
            raise Exception("i2c: data should be under 1024 bytes")

        obj = {}
        obj["i2c" + str(self.id)] = {"address": address, "data": data}
        self.obniz.send(obj)

    def read_wait(self, address, length):
        if not self.used:
            raise Exception("i2c{} is not started".format(self.id))

        address = int(address)
        if not address:
            raise Exception("i2c: please specify address")

        if address < 0 or address > 0x7F:
            raise Exception("i2c: invalid address")

        length = int(length)
        if not length or length < 0:
            raise Exception("i2c: invalid length to read")

        if length > 1024:
            raise Exception("i2c: data length should be under 1024 bytes")

        future = asyncio.get_event_loop().create_future()
        self.add_observer(future)
        obj = {}
        obj["i2c" + str(self.id)] = {"address": address, "read": length}
        self.obniz.send(obj)
        return future

    def notified(self, obj):
        if obj and type(obj) is dict:
            if "data" in obj:
                if obj["mode"] == "slave" and self.onwritten:
                    self.onwritten(obj["data"], obj["address"])
                else:
                    # TODO: we should compare byte length from sent
                    if len(self.observers) > 0:
                        future = self.observers.pop(0)
                        future.set_result(obj["data"])
            if "warning" in obj:
                self.obniz.warning(
                    {
                        "alert": "warning",
                        "message": "i2c{}: {}".format(
                            self.id, obj["warning"]["message"]
                        ),
                    }
                )

            if "error" in obj:
                self.obniz.error(
                    {
                        "alert": "error",
                        "message": "i2c{}: {}".format(self.id, obj["error"]["message"]),
                    }
                )

    def is_used(self):
        return self.used

    def end(self):
        self.state = {}
        obj = {}
        obj["i2c" + str(self.id)] = None
        self.obniz.send(obj)
        self.used = False
