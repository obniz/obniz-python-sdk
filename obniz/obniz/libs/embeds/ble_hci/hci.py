
class ObnizBLEHci:
    def __init__(self, Obniz):
        self.Obniz = Obniz

    def write(self, hciCommand):
        self.Obniz.send({
            "ble": {
                "hci": {
                    "write": hciCommand
                }
            }
        })

    def notified(self, obj):
        if "read" in obj and "data" in obj["read"]:
            self.onread(obj["read"]["data"])

    def onread(self, _):
        pass