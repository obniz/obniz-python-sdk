from attrdict import AttrDefault
import asyncio

class HCSR505:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'signal']
        self.required_keys = ['signal']

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'HC-SR505'})

    def wired(self, obniz):
        self.obniz = obniz
        self.io_signal = obniz.get_io(*[self.params.signal])
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        def setval(val):
            if self.onchange:
                self.onchange(val)
        self.io_signal.input(setval)

    def get_wait(self):
        async def getval():
            val = await self.io_signal.input_wait()
            return val
        return getval()