from ..utils.util import ObnizUtil


class PeripheralUART:
    def __init__(self, obniz, id):
        self.obniz = obniz
        self.id = id
        self.onreceive = None
        self._reset()

    def _reset(self):
        # TODO: Uint8Array
        # self.received = new Uint8Array([])
        self.received = []
        self.used = False

    def start(self, params):
        err = ObnizUtil._required_keys(params, ["tx", "rx"])
        if err:
            raise Exception("uart start param '" + err + "' required, but not found ")

        self.params = ObnizUtil._key_filter(
            params,
            [
                "tx",
                "rx",
                "baud",
                "stop",
                "bits",
                "parity",
                "flowcontrol",
                "rts",
                "cts",
                "drive",
                "pull",
                "gnd",
            ],
        )

        io_keys = ["rx", "tx", "rts", "cts", "gnd"]
        for key in io_keys:
            if key in self.params and not self.obniz.is_valid_io(self.params[key]):
                raise Exception("uart start param '" + key + "' are to be valid io no")

        if "drive" in self.params:
            self.obniz.get_io(self.params["rx"]).drive(self.params["drive"])
            self.obniz.get_io(self.params["tx"]).drive(self.params.drive)
        else:
            self.obniz.get_io(self.params["rx"]).drive("5v")
            self.obniz.get_io(self.params["tx"]).drive("5v")

        if "pull" in self.params:
            self.obniz.get_io(self.params["rx"]).pull(self.params["pull"])
            self.obniz.get_io(self.params["tx"]).pull(self.params["pull"])
        else:
            self.obniz.get_io(self.params["rx"]).pull(None)
            self.obniz.get_io(self.params["tx"]).pull(None)

        if "gnd" in self.params:
            self.obniz.get_io(self.params["gnd"]).output(False)
            # TODO: display無い場合の挙動確認
            # io_names = {}
            # io_names[self.params["gnd"]] = 'gnd'
            # self.obniz.display.setPinNames('uart' + self.id, io_names)

        obj = {}
        send_params = ObnizUtil._key_filter(
            self.params,
            ["tx", "rx", "baud", "stop", "bits", "parity", "flowcontrol", "rts", "cts"],
        )
        obj["uart" + str(self.id)] = send_params
        self.obniz.send(obj)
        self.received = []
        self.used = True

    def send(self, data):
        if not self.used:
            raise Exception("uart{} is not started".format(self.id))

        send_data = None
        if data is None:
            return

        if type(data) is int:
            data = [data]

        # if (isNode && data instanceof Buffer) {
        #     send_data = [...data]
        if type(data) is list:
            send_data = data
        elif type(data) is str:
            send_data = ObnizUtil.string2data_array(data)

        obj = {}
        obj["uart" + str(self.id)] = {}
        obj["uart" + str(self.id)]["data"] = send_data
        self.obniz.send(obj)

    def is_data_exists(self):
        return self.received and len(self.received) > 0

    def read_bytes(self):
        results = []
        if self.is_data_exists():
            for result in self.received:
                results.append(result)

        self.received = []
        return results

    def read_text(self):
        string = None
        if self.is_data_exists():
            data = self.read_bytes()
            string = self.try_convert_string(data)

        self.received = []
        return string

    def try_convert_string(self, data):
        return ObnizUtil.data_array2string(data)

    def notified(self, obj):
        if self.onreceive:
            string = self.try_convert_string(obj["data"])
            self.onreceive(obj["data"], string)
        else:
            if not self.received:
                self.received = []

            self.received.extend(obj["data"])

    # isUsed() {
    #     return self.used
    # }

    def end(self):
        obj = {}
        obj["uart" + str(self.id)] = None
        self.params = None
        self.obniz.send(obj)
        self.used = False
