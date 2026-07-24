from ..utils.eventloop import get_event_loop

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

    def add_observer(self, future):
        if future:
            self.observers.append(future)

    def get_wait(self):
        future = get_event_loop().create_future()
        self.add_observer(future)
        obj = {}
        obj["switch"] = "get"
        self.obniz.send(obj)
        return future

    def state_wait(self, is_pressed):
        future = get_event_loop().create_future()
        def on_change_for_state_wait(pressed):
            def noop(*args):
                pass
            if is_pressed == pressed:
                self.on_change_for_state_wait = noop
                future.set_result(None)
        self.on_change_for_state_wait = on_change_for_state_wait
        return future

    def notified(self, obj):
        self.state = obj["state"]
        if self.onchange:
            self.onchange(self.state)

        self.on_change_for_state_wait(self.state)

        if len(self.observers) > 0:
            future = self.observers.pop(0)
            future.set_result(self.state)