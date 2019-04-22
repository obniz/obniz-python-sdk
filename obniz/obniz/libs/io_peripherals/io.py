import asyncio

class PeripheralIO:
    def __init__(self, obniz, id):
        self.obniz = obniz
        self.id = id
        self.onchange = None
        self._reset()

    def _reset(self):
        self.value = 0
        self.observers = []

    def add_observer(self, callback):
        if callback:
            self.observers.append(callback)

    def output(self, value):
        value = bool(value)
        obj = {}
        obj["io" + str(self.id)] = value
        self.value = value
        self.obniz.send(obj)

    def drive(self, drive):
        if type(drive) is not str:
            raise Exception("please specify drive methods in string")

        if drive == "5v":
            output_type = "push-pull5v"
        elif drive == "3v":
            output_type = "push-pull3v"
        elif drive == "open-drain":
            output_type = "open-drain"
        else:
            raise Exception("unknown drive method")

        obj = {}
        obj["io" + str(self.id)] = {"output_type": output_type}
        self.obniz.send(obj)

    def pull(self, updown):
        if updown is not None and type(updown) is not str:
            raise Exception("please specify pull methods in string")

        if updown == "5v" or updown == "pull-up5v":
            pull_type = "pull-up5v"
        elif updown == "3v" or updown == "pull-up3v":
            pull_type = "pull-up3v"
        elif updown == "0v" or updown == "pull-down":
            pull_type = "pull-down"
        elif updown is None or updown == "float":
            pull_type = "float"
        else:
            raise Exception("unknown pull_type method")

        obj = {}
        obj["io" + str(self.id)] = {"pull_type": pull_type}
        self.obniz.send(obj)

    def input(self, callback):
        self.onchange = callback
        obj = {}
        obj["io" + str(self.id)] = {"direction": "input", "stream": True}
        self.obniz.send(obj)
        return self.value

    def input_wait(self):
        future = asyncio.get_event_loop().create_future()
        self.add_observer(future)
        obj = {}
        obj["io" + str(self.id)] = {"direction": "input", "stream": False}
        self.obniz.send(obj)
        return future

    def end(self):
        obj = {}
        obj["io" + str(self.id)] = None
        self.obniz.send(obj)

    def notified(self, obj):
        if type(obj) is bool:
            self.value = obj
            if len(self.observers) > 0:
                item = self.observers.pop(0)
                if callable(item): # callback
                    item(obj)
                else: # future
                    item.set_result(obj)

            if self.onchange:
                self.onchange(obj)

        elif type(obj) is object:
            if obj.warning:
                self.obniz.warning(
                    {
                        "alert": "warning",
                        "message": "io{}: {}".format(self.id, obj.warning.message),
                    }
                )

            if obj.error:
                self.obniz.error(
                    {
                        "alert": "error",
                        "message": "io{}}: {}".format(self.id, obj.error.message),
                    }
                )


# }
