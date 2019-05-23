import asyncio
import datetime


class PeripheralIO_:  # noqa: N801
    def __init__(self, obniz):
        self.obniz = obniz
        self.observers = []
        self._reset()
    
    def _reset(self):
        for observer in self.observers:
            observer.cancel()
        self.observers.clear()
        self._animation_identifier = 0

    def add_observer(self, name, future):
        if asyncio.isfuture(future):
            self.observers.append({
                "future": future,
                "name": name
            })

    def animation(self, name, status, array=None, repeat=None):
        obj = {}
        obj["io"] = {"animation": {"name": name, "status": status}}
        if type(repeat) is int:
            obj["io"]["animation"]["repeat"] = repeat
        if array is None:
            array = []

        states = []
        for i in range(0, len(array)):
            state = array[i]
            duration = state["duration"]
            operation = state["state"]

            # dry run. and get json commands
            self.obniz.send_pool = []
            operation(i)
            pooled_json_array = self.obniz.send_pool
            self.obniz.send_pool = None
            states.append({"duration": duration, "state": pooled_json_array})

        if status == "loop":
            obj["io"]["animation"]["states"] = states

        self.obniz.send(obj)

    def repeat_wait(self, array, repeat):
        if (type(repeat) not in [int, float] or repeat < 1):
            raise Exception("please specify repeat count > 0")
        if (type(repeat) is not int):
            raise Exception("please provide integer number like 1, 2, 3,,,")
        
        # get_running_loop() function is preferred on Python >= 3.7
        future = asyncio.get_event_loop().create_future()
        name = "_repeatwait" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if self._animation_identifier + 1 > 1000:
            self._animation_identifier = 0
        
        self.animation(name, "loop", array, repeat)
        self.add_observer(name, future)
        return future

    def notified(self, obj):
        if obj["animation"]["status"] == "finish":
            matched_list = [observer for observer in self.observers if obj["animation"]["name"] == observer["name"]]
            for matched in matched_list:
                matched["future"].set_result(None)
                self.observers.remove(matched)
