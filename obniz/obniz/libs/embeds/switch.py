class ObnizSwitch:
    def __init__(self, obniz):
        self.obniz = obniz
        self.onchange = None
        self._reset()

    def _reset(self):
        self.observers = []

        def noop(state):
            pass

        self.on_change_for_state_wait = noop

    def add_observer(self, callback):
        if callback:
            self.observers.append(callback)

    def get_wait(self, callback):
        obj = {}
        obj["switch"] = "get"
        self.obniz.send(obj)
        self.add_observer(callback)

    def state_wait(self, is_pressed, callback):
        def on_change_for_state_wait(pressed):
            if is_pressed == pressed:
                self.onChangeForStateWait = callback

        self.on_change_for_state_wait = on_change_for_state_wait

    def notified(self, obj):
        self.state = obj["state"]
        if self.onchange:
            self.onchange(self.state)

        self.on_change_for_state_wait(self.state)

        if len(self.observers) > 0:
            callback = self.observers.pop(0)
            callback(self.state)
