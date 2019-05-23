from ..utils.util import ObnizUtil


class PeripheralPWM:
    def __init__(self, obniz, id):
        self.obniz = obniz
        self.id = id
        self._reset()

    def _reset(self):
        self.state = {}
        self.used = False

    def send_ws(self, obj):
        ws_obj = {}
        ws_obj["pwm" + str(self.id)] = obj
        self.obniz.send(ws_obj)

    def start(self, params):
        err = ObnizUtil._required_keys(params, ["io"])
        if err:
            raise Exception("pwm start param '" + err + "' required, but not found ")

        self.params = ObnizUtil._key_filter(params, ["io", "drive", "pull"])

        io = self.params["io"]
        io_obj = self.obniz.get_io(io)

        io_obj.drive(self.params.get("drive", "5v"))
        io_obj.pull(self.params.get("pull"))

        self.state = {"io": io, "freq": 1000}
        self.send_ws({"io": io})
        self.used = True

    def freq(self, freq):
        if not self.used:
            raise Exception("pwm{} is not started".format(self.id))

        freq *= 1
        if type(freq) is not int:
            raise Exception("please provide freq in number")

        self.state["freq"] = freq
        self.send_ws({"freq": freq})
        if type(self.state.get("duty")) is int:
            self.duty(self.state["duty"])

    def pulse(self, pulse_width):
        if not self.used:
            raise Exception("pwm{} is not started".format(self.id))

        self.state["pulse"] = pulse_width
        if "duty" in self.state:
            del self.state["duty"]
        self.send_ws({"pulse": pulse_width})

    def duty(self, duty):
        if not self.used:
            raise Exception("pwm{} is not started".format(self.id))

        duty *= 1
        if type(self.state["freq"]) is not int or self.state["freq"] <= 0:
            raise Exception("please provide freq first.")

        if type(duty) not in  [int, float]:
            raise Exception("please provide duty in number")

        if duty < 0:
            duty = 0

        if duty > 100:
            duty = 100

        pulse_width = (1.0 / self.state["freq"]) * 1000 * duty * 0.01
        self.state["duty"] = duty
        self.send_ws({"pulse": pulse_width})

    def is_used(self):
        return self.used

    def end(self):
        self.state = {}
        self.send_ws(None)
        self.used = False

    def modulate(self, type, symbol_length, data):
        if not self.used:
            raise Exception("pwm{} is not started".format(self.id))

        self.send_ws(
            {"modulate": {"type": type, "symbol_length": symbol_length, "data": data}}
        )
