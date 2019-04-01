from attrdict import AttrDefault

import asyncio

class KXR942050:
    def __init__(self):
        self.keys = ['x', 'y', 'z', 'vcc', 'gnd', 'enable', 'self_test']
        self.required_keys = ['x', 'y', 'z']
        self.on_change = None
        self.on_change_x = self.on_change_y = self.on_change_z = None
        self._x_val = self._y_val = self._z_val = 0

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'KXR94-2050'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.ad_x = obniz.get_ad(*[self.params.x])
        self.ad_y = obniz.get_ad(*[self.params.y])
        self.ad_z = obniz.get_ad(*[self.params.z])
        if obniz.is_valid_io(*[self.params.enable]):
            obniz.get_io(*[self.params.enable]).drive(*['5v'])
            obniz.get_io(*[self.params.enable]).output(*[True])
            obniz.display.set_pin_name(*[self.params.enable, 'KXR94_2050', 'E'])
        if obniz.is_valid_io(*[self.params.self_test]):
            obniz.get_io(*[self.params.self_test]).drive(*['5v'])
            obniz.get_io(*[self.params.self_test]).output(*[False])
            obniz.display.set_pin_name(*[self.params.self_test, 'KXR94_2050', 'T'])
        self.change_vcc_voltage(*[5])
        
        def set_x(value):
            self._x_val = value
            if self.on_change_x:
                self.on_change_x(self.voltage2gravity(value))
            if self.on_change:
                self.on_change(self._get())
        self.ad_x.start(set_x)
        def set_y(value):
            self._y_val = value
            if self.on_change_y:
                self.on_change_y(self.voltage2gravity(value))
            if self.on_change:
                self.on_change(self._get())
        self.ad_y.start(set_y)
        def set_z(value):
            self._z_val = value
            if self.on_change_z:
                self.on_change_z(self.voltage2gravity(value))
            if self.on_change:
                self.on_change(self._get())
        self.ad_z.start(set_z)
        
        if self.obniz.is_valid_io(*[self.params.vcc]):
            self.obniz.get_ad(*[self.params.vcc]).start(lambda value: self.change_vcc_voltage(value))
        
        obniz.display.set_pin_name(*[self.params.x, 'KXR94_2050', 'x'])
        obniz.display.set_pin_name(*[self.params.y, 'KXR94_2050', 'y'])
        obniz.display.set_pin_name(*[self.params.z, 'KXR94_2050', 'z'])
        if self.obniz.is_valid_io(*[self.params.vcc]):
            obniz.display.set_pin_name(*[self.params.vcc, 'KXR94_2050', 'vcc'])

    def change_vcc_voltage(self, pwr_voltage):
        self.sensitivity = pwr_voltage / 5
        self.offset_voltage = pwr_voltage / 2

    def voltage2gravity(self, volt):
        return (volt - self.offset_voltage) / self.sensitivity

    def get(self):
        return self._get()

    def _get(self):
        return AttrDefault(bool, {'x': self.voltage2gravity(*[self._x_val]), 'y': self.voltage2gravity(*[self._y_val]), 'z': self.voltage2gravity(*[self._z_val])})

    def get_wait(self):
        async def getval():
            self._x_val = await self.ad_x.get_wait()
            self._y_val = await self.ad_y.get_wait()
            self._z_val = await self.ad_z.get_wait()
            return self._get()
        return getval()