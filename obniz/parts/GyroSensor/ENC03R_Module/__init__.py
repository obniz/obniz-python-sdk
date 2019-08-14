from attrdict import AttrDefault

import asyncio

class ENC03R_Module:
    def __init__(self):
        self.keys = ['vcc', 'out1', 'out2', 'gnd']
        self.required_keys = ['out1', 'out2']
        self._sens = 0.00067
        self.onchange1 = self.onchange2 = None

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'ENC03R_Module'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.ad0 = obniz.get_ad(*[self.params.out1])
        self.ad1 = obniz.get_ad(*[self.params.out2])
        def anonymous0(value):
            self.sens1 = (value - 1.45) / self._sens
            if self.onchange1:
                self.onchange1(*[self.sens1])
        self.ad0.start(*[anonymous0])
        def anonymous1(value):
            self.sens2 = (value - 1.35) / self._sens
            if self.onchange2:
                self.onchange2(*[self.sens2])
        self.ad1.start(*[anonymous1])

    def get1_wait(self):
        future = asyncio.get_event_loop().create_future()
        async def anonymous2():
            value = await self.ad0.get_wait(*[])
            self.sens1 = (value - 1.45) / self._sens
            return self.sens1
        return anonymous2()

    def get2_wait(self):
        future = asyncio.get_event_loop().create_future()
        async def anonymous3():
            value = await self.ad1.get_wait(*[])
            self.sens2 = (value - 1.35) / self._sens
            return self.sens2
        return anonymous3()