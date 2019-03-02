class PeripheralIO_:  # noqa: N801
    def __init__(self, obniz):
        self.obniz = obniz

    def animation(self, name, status, array=None):
        obj = {}
        obj["io"] = {"animation": {"name": name, "status": status}}
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
