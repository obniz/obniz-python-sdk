from ..utils.util import ObnizUtil


class LogicAnalyzer:
    def __init__(self, obniz):
        self.obniz = obniz
        self._reset()

    def _reset(self):
        self.onmeasured = None

    def start(self, params):
        err = ObnizUtil._required_keys(params, ["io", "interval", "duration"])
        if err:
            raise Exception(
                "LogicAnalyzer start param '" + err + "' required, but not found "
            )

        self.params = ObnizUtil._key_filter(
            params,
            ["io", "interval", "duration", "triggerValue", "triggerValueSamples"],
        )

        obj = {}
        obj["logic_analyzer"] = {
            "io": [self.params["io"]],
            "interval": self.params["interval"],
            "duration": self.params["duration"],
        }
        if self.params.get("triggerValueSamples", 0) > 0:
            obj["logic_analyzer"]["trigger"] = {
                "value": bool(self.params["triggerValue"]),
                "samples": self.params["triggerValueSamples"],
            }

        self.obniz.send(obj)

    def end(self):
        obj = {}
        obj["logic_analyzer"] = None
        self.obniz.send(obj)

    def notified(self, obj):
        if self.onmeasured:
            self.onmeasured(obj["data"])
        else:
            if not self.measured:
                self.measured = []

            self.measured.push(obj["data"])
