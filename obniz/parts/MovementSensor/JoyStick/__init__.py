from attrdict import AttrDefault

import asyncio

class JoyStick:
    def __init__(self):
        self.keys = ['sw', 'y', 'x', 'vcc', 'gnd', 'i2c']
        self.required_keys = ['sw', 'y', 'x']
        self.pins = self.keys or ['sw', 'y', 'x', 'vcc', 'gnd']
        self.pinname = AttrDefault(bool, {'sw': 'sw12'})
        self.short_name = 'joyS'
        self.onchangex = self.onchangey = self.onchangesw = None

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'JoyStick'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.io_sig_sw = obniz.get_io(*[self.params.sw])
        self.ad_x = obniz.get_ad(*[self.params.x])
        self.ad_y = obniz.get_ad(*[self.params.y])
        self.io_sig_sw.pull(*['5v'])

        def setx(val):
            self.position_x = val / 5.0
            if self.onchangex:
                self.onchangex(self.position_x * 2 - 1)
        self.ad_x.start(setx)
        def sety(val):
            self.position_y = val / 5.0
            if self.onchangey:
                self.onchangey(self.position_y * 2 - 1)
        self.ad_y.start(sety)
        def setsw(val):
            self.is_pressed = val == False
            if self.onchangesw:
                self.onchangesw(self.is_pressed)
        self.io_sig_sw.input(setsw)

    async def is_pressed_wait(self):
        ret = await self.io_sig_sw.input_wait()
        return ret == False

    async def get_x_wait(self):
        value = await self.ad_x.get_wait()
        self.position_x = value / 5.0
        return (self.position_x * 2 - 1)

    async def get_y_wait(self):
        value = await self.ad_y.get_wait()
        self.position_y = value / 5.0
        return (self.position_y * 2 - 1)