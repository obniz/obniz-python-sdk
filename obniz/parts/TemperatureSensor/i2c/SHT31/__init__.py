from attrdict import AttrDefault

import asyncio

class SHT31:
    def __init__(self):
        self.required_keys = ['adr', 'addressmode']
        self.keys = ['vcc', 'sda', 'scl', 'gnd', 'adr', 'addressmode', 'i2c', 'pull']
        self.io_keys = ['vcc', 'sda', 'scl', 'gnd', 'adr']
        self.commands = AttrDefault(bool, {})
        self.commands.soft_reset = [0x30, 0xa2]
        self.commands.high_repeat_streach = [0x2c, 0x06]
        self.commands.middle_repeat_streach = [0x2c, 0x0d]
        self.commands.low_repeat_streach = [0x2c, 0x10]
        self.commands.high_repeat = [0x24, 0x00]
        self.commands.medium_repeat = [0x24, 0x0b]
        self.commands.low_repeat = [0x24, 0x16]
        self.wait_time = AttrDefault(bool, {})
        self.wait_time.wakeup = 1
        self.wait_time.soft_reset = 1
        self.wait_time.low_repeat = 4
        self.wait_time.medium_repeat = 6
        self.wait_time.high_repeat = 15
        self.commands.read_status = [0xf3, 0x2d]

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'SHT31'})

    def wired(self, obniz):
        self.obniz = obniz
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.io_adr = obniz.get_io(*[self.params.adr])
        if self.params.addressmode == 4:
            self.io_adr.output(*[False])
            self.address = 0x44
        elif self.params.addressmode == 5:
            self.io_adr.pull(*[None])
            self.address = 0x45
        self.params.clock = self.params.clock or 100 * 1000
        self.params.mode = self.params.mode or 'master'
        self.params.pull = self.params.pull or '5v'
        self.i2c = obniz.get_i2c_with_config(*[self.params])
        obniz.i2c0.write(*[self.address, self.commands.soft_reset])

    async def get_data(self):
        self.i2c.write(*[self.address, self.commands.high_repeat])
        await self.obniz.wait(*[self.wait_time.high_repeat])
        return await self.i2c.read_wait(*[self.address, 6])

    async def get_temp_wait(self):
        obj = await self.get_all_wait()
        return obj.temperature

    async def get_humd_wait(self):
        obj = await self.get_all_wait()
        return obj.humidity

    async def get_all_wait(self):
        ret = await self.get_data()
        temp_bin = (ret[0] * 256 + ret[1])
        temperature = (-45 + 175 * temp_bin / (65536 - 1))
        humd_bin = (ret[3] * 256 + ret[4])
        humidity = 100 * humd_bin / (65536 - 1)
        return AttrDefault(bool, {'temperature': temperature, 'humidity': humidity})