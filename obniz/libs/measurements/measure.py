from ..utils.util import ObnizUtil


class ObnizMeasure:
    def __init__(self, obniz):
        self.obniz = obniz
        self._reset()

    def _reset(self):
        self.observers = []

    def echo(self, params):
        err = ObnizUtil._required_keys(
            params, ["io_pulse", "pulse", "pulse_width", "io_echo", "measure_edges"]
        )
        if err:
            raise Exception(
                "Measure start param '" + err + "' required, but not found "
            )

        self.params = ObnizUtil._key_filter(
            params,
            [
                "io_pulse",
                "pulse",
                "pulse_width",
                "io_echo",
                "measure_edges",
                "timeout",
                "callback",
            ],
        )

        echo = {}
        echo["io_pulse"] = self.params["io_pulse"]
        echo["pulse"] = self.params["pulse"]
        echo["pulse_width"] = self.params["pulse_width"]
        echo["io_echo"] = self.params["io_echo"]
        echo["measure_edges"] = self.params["measure_edges"]
        if type(self.params.get("timeout")) is int:
            echo["timeout"] = self.params["timeout"]

        self.obniz.send({"measure": {"echo": echo}})

        if "callback" in self.params:
            self.observers.append(self.params["callback"])

    def notified(self, obj):
        if len(self.observers):
            callback = self.observers.pop(0)
            callback(obj["echo"])
