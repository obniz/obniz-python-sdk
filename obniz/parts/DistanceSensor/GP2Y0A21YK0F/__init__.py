from attrdict import AttrDefault

import asyncio
import math

class GP2Y0A21YK0F:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'signal']
        self.required_keys = ['signal']
        self.display_io_names = AttrDefault(bool, {'vcc': 'vcc', 'gnd': 'gnd', 'signal': 'signal'})
        self._unit = 'mm'

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'GP2Y0A21YK0F'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.io_signal = obniz.get_io(*[self.params.signal])
        self.io_signal.end()
        self.ad_signal = obniz.get_ad(*[self.params.signal])

    def start(self, callback):
        def ret_distance(val):
            distance = self._volt2distance(val)
            if callable(callback):
                callback(distance)
        self.ad_signal.start(ret_distance)

    def _volt2distance(self, val):
        if val <= 0:
            val = 0.001
        distance = 19988.34 * math.pow(*[val / 5.0 * 1024, -1.25214]) * 10
        if self._unit == 'mm':
            distance = int(*[distance * 10]) / 10
        else:
            distance *= 0.0393701
            distance = int(*[distance * 1000]) / 1000
        return distance

    def get_wait(self):
        async def get_distance():
            val = await self.ad_signal.get_wait()
            distance = self._volt2distance(val)
            return distance
        return get_distance()

    def unit(self, unit):
        if unit == 'mm':
            self._unit = 'mm'
        elif unit == 'inch':
            self._unit = 'inch'
        else:
            raise Exception('unknown unit ' + str(unit))