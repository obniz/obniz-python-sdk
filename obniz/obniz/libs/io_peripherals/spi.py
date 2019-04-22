from distutils.version import LooseVersion

from ..utils.util import ObnizUtil

import asyncio
import semver

class PeripheralSPI:
    def __init__(self, obniz, id):
        self.obniz = obniz
        self.id = id
        self._reset()

    def _reset(self):
        self.observers = []
        self.used = False

    def add_observer(self, callback):
        if callback:
            self.observers.append(callback)

    def start(self, params):
        err = ObnizUtil._required_keys(params, ["mode", "frequency"])
        if err:
            raise Exception("spi start param '" + err + "' required, but not found ")

        self.params = ObnizUtil._key_filter(
            params, ["mode", "clk", "mosi", "miso", "frequency", "drive", "pull", "gnd"]
        )
        obj = {}

        io_keys = ["clk", "mosi", "miso", "gnd"]
        for key in io_keys:
            if key in self.params and not self.obniz.is_valid_io(self.params[key]):
                raise Exception("spi start param '" + key + "' are to be valid io no")

        obj["spi" + str(self.id)] = {
            "mode": self.params["mode"],
            "clock": self.params["frequency"],  # name different
        }
        if "clk" in self.params:
            obj["spi" + str(self.id)]["clk"] = self.params["clk"]

        if "mosi" in self.params:
            obj["spi" + str(self.id)]["mosi"] = self.params["mosi"]

        if "miso" in self.params:
            obj["spi" + str(self.id)]["miso"] = self.params["miso"]

        if "drive" in self.params:
            if "clk" in self.params:
                self.obniz.get_io(self.params["clk"]).drive(self.params["drive"])
            if "mosi" in self.params:
                self.obniz.get_io(self.params["mosi"]).drive(self.params["drive"])
            if "miso" in self.params:
                self.obniz.get_io(self.params["miso"]).drive(self.params["drive"])
        else:
            if "clk" in self.params:
                self.obniz.get_io(self.params["clk"]).drive("5v")
            if "mosi" in self.params:
                self.obniz.get_io(self.params["mosi"]).drive("5v")
            if "miso" in self.params:
                self.obniz.get_io(self.params["miso"]).drive("5v")

        if "pull" in self.params:
            if "clk" in self.params:
                self.obniz.get_io(self.params["clk"]).pull(self.params["pull"])
            if "mosi" in self.params:
                self.obniz.get_io(self.params["mosi"]).pull(self.params["pull"])
            if "miso" in self.params:
                self.obniz.get_io(self.params["miso"]).pull(self.params["pull"])
        else:
            if "clk" in self.params:
                self.obniz.get_io(self.params["clk"]).pull(None)
            if "mosi" in self.params:
                self.obniz.get_io(self.params["mosi"]).pull(None)
            if "miso" in self.params:
                self.obniz.get_io(self.params["miso"]).pull(None)

        if "gnd" in self.params:
            self.obniz.get_io(self.params["gnd"]).output(False)
            # TODO: display無い場合の挙動確認
            # ioNames = {}
            # ioNames[self.params.gnd] = 'gnd'
            # self.obniz.display.setPinNames('spi' + str(self.id), ioNames)

        self.used = True
        self.obniz.send(obj)

    def write_wait(self, data):
        if not self.used:
            raise Exception("spi{} is not started".format(self.id))

        if (
            LooseVersion(self.obniz.firmware_ver) <= LooseVersion("1.0.2")
            and len(data) > 32
        ):
            raise Exception(
                "with your obniz "
                + self.obniz.firmware_ver
                + ". "
                + "spi max length=32byte but yours "
                + str(len(data))
                + ". Please update obniz firmware"
            )

        future = asyncio.get_event_loop().create_future()
        self.add_observer(future)
        obj = {}
        obj["spi" + str(self.id)] = {"data": data, "read": True}
        self.obniz.send(obj)
        return future

    def write(self, data):
        if not self.used:
            raise Exception("spi{0} is not started".format(self.id))
        if semver.match(self.obniz.firmware_ver, "<=1.0.2") and len(data) > 32:
            raise Exception(
                "with your obniz {0}. spi max length=32byte but yours {1}. Please update obniz firmware".format(
                    self.obniz.firmware_ver, len(data)
                )
            )

        obj = {}
        obj['spi' + str(self.id)] = {
            "data": data,
            "read": False
        }
        self.obniz.send(obj)

    def notified(self, obj):
        # TODO: we should compare byte length from sent
        if len(self.observers) > 0:
            callback = self.observers.pop(0)
            # callback(obj["data"])
            callback.set_result(obj["data"])

    def is_used(self):
        return self.used

    def end(self, reuse=None):
        obj = {}
        obj["spi" + str(self.id)] = None
        self.params = None
        self.obniz.send(obj)
        if not reuse:
            self.used = False
