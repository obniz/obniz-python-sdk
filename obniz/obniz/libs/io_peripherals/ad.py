class PeripheralAD:
    def __init__(self, obniz, id):
        self.obniz = obniz
        self.id = id
        self.onchange = None
        self._reset()

    def _reset(self):
        self.value = 0.0
        self.observers = []

    def add_observer(self, callback):
        if callback:
            self.observers.append(callback)

    def start(self, callback=None):
        self.onchange = callback
        obj = {}
        obj["ad" + str(self.id)] = {"stream": True}
        self.obniz.send(obj)
        return self.value

    def get_wait(self, callback):
        self.add_observer(callback)
        obj = {}
        obj["ad" + str(self.id)] = {"stream": False}
        self.obniz.send(obj)

    def end(self):
        self.onchange = None
        obj = {}
        obj["ad" + str(self.id)] = None
        self.obniz.send(obj)

    def notified(self, obj):
        self.value = obj
        if self.onchange:
            self.onchange(obj)

        if len(self.observers) > 0:
            callback = self.observers.pop(0)
            callback(obj)
