from attrdict import AttrDefault

import asyncio

class Button:
    def __init__(self):
        def nothing(*args):
            pass
        self.keys = ['signal', 'gnd']
        self.required_keys = ['signal']
        self.onchange = None
        self.on_change_for_state_wait = nothing

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'Button'})

    def wired(self, obniz):
        self.io_signal = obniz.get_io(*[self.params.signal])
        if obniz.is_valid_io(*[self.params.gnd]):
            self.io_supply = obniz.get_io(*[self.params.gnd])
            self.io_supply.output(*[False])
        self.io_signal.pull(*['5v'])
        def getval(value):
            self.is_pressed = (value == False)
            if self.onchange:
                self.onchange(value == False)
            self.on_change_for_state_wait(value == False)
        self.io_signal.input(getval)

    async def is_pressed_wait(self):
        ret = await self.io_signal.input_wait()
        return ret == False

    def state_wait(self, is_pressed):
        # get_running_loop() function is preferred on Python >= 3.7
        future = asyncio.get_event_loop().create_future()
        def onpress(pressed):
            def nothing(*args):
                pass
            if is_pressed == pressed:
                self.on_change_for_state_wait = nothing
                future.set_result(None)
        self.on_change_for_state_wait = onpress
        return future