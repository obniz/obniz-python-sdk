from attrdict import AttrDefault

import asyncio

class FSR40X:
    def __init__(self):
        self.keys = ['pin0', 'pin1']
        self.required_keys = ['pin0', 'pin1']
        self.onchange = None

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'FSR40X'})

    def wired(self, obniz):
        self.obniz = obniz
        self.io_pwr = obniz.get_io(*[self.params.pin0])
        self.ad = obniz.get_ad(*[self.params.pin1])
        self.io_pwr.drive(*['5v'])
        self.io_pwr.output(*[True])
        def get_pressure(value):
            pressure = value * 100
            self.press = pressure
            if self.onchange:
                self.onchange(self.press)
        self.ad.start(get_pressure)

    async def get_wait(self):
        value = await self.ad.get_wait()
        pressure = value * 100
        self.press = pressure
        return self.press