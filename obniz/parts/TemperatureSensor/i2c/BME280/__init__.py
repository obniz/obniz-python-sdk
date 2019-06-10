import asyncio
import math

from attrdict import AttrDefault

class BME280:
    def __init__(self):
        self.required_keys = []
        self.keys = ['vcore', 'vio', 'gnd', 'csb', 'sdi', 'sck', 'sdo', 'i2c', 'address']
        self.io_keys = ['vcore', 'vio', 'gnd', 'csb', 'sdi', 'sdo', 'sck']
        self.configration = AttrDefault(bool, {'sampling': AttrDefault(bool, {'temp': 1, 'hum': 1, 'pres': 1}), 'interval': 5, 'iir_strength': 0, 'mode': 3, '_modes': AttrDefault(bool, {'sleep': 0, 'forced': 1, 'normal': 3})})
        self.commands = AttrDefault(bool, {})
        self.commands.addresses = AttrDefault(bool, {'config': 0xf5, 'ctrl_meas': 0xf4, 'ctrl_hum': 0xf2})

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'BME280', 'datasheet': 'https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BME280_DS001-12.pdf'})

    def wired(self, obniz):
        self.obniz = obniz
        if obniz.is_valid_io(*[self.params.csb]):
            self.io_csb = obniz.get_io(*[self.params.csb])
            self.io_csb.drive(*['3v'])
            self.io_csb.output(*[True])
        self.obniz.set_vcc_gnd(*[self.params.vio, None, '3v'])
        self.obniz.set_vcc_gnd(*[self.params.vcore, None, '3v'])
        self.obniz.set_vcc_gnd(*[None, self.params.gnd, '5v'])
        self.obniz.wait(*[10])
        self.address = 0x76
        if self.params.address == 0x76:
            self.address = 0x76
        elif self.params.address == 0x77:
            self.address = 0x77
        elif self.params.address:
            raise Exception('address must be 0x76 or 0x77')
        if obniz.is_valid_io(*[self.params.sdo]):
            self.io_sdo = obniz.get_io(*[self.params.sdo])
            self.io_sdo.drive(*['3v'])
            self.io_sdo.output(*[False if self.address == 0x76 else True])
        self.params.sda = self.params.sda or self.params.sdi
        self.params.scl = self.params.scl or self.params.sck
        self.params.clock = self.params.clock or 100 * 1000
        self.params.mode = 'master'
        self.params.pull = '3v'
        self.i2c = obniz.get_i2c_with_config(*[self.params])
        self.obniz.wait(*[10])
        self.config()
        self.obniz.wait(*[10])

    def config(self):
        self.write(*[[self.commands.addresses.config, self.configration.interval << 5 | self.configration.iir_strength << 2 | 0]])
        self.write(*[[self.commands.addresses.ctrl_hum, self.configration.sampling.hum]])
        self.write(*[[self.commands.addresses.ctrl_meas, self.configration.sampling.temp << 5 | self.configration.sampling.pres << 2 | self.configration.mode]])

    def set_iir_strength(self, strengh):
        self.configration.iir_strength = strengh
        self.config()

    async def apply_calibration(self):
        self.i2c.write(*[self.address, [0x88]])
        data = await self.i2c.read_wait(*[self.address, 24])
        self.i2c.write(*[self.address, [0xa1]])
        data_next = await self.i2c.read_wait(*[self.address, 1])
        data.extend(*[data_next])
        self.i2c.write(*[self.address, [0xe1]])
        data_next = await self.i2c.read_wait(*[self.address, 7])
        data.extend(*[data_next])
        self._calibrated = AttrDefault(bool,
            {
                'dig_t1': data[1] << 8 | data[0],
                'dig_t2': self._read_signed16(*[data[3] << 8 | data[2]]),
                'dig_t3': self._read_signed16(*[data[5] << 8 | data[4]]),
                'dig_p1': data[7] << 8 | data[6],
                'dig_p2': self._read_signed16(*[data[9] << 8 | data[8]]),
                'dig_p3': self._read_signed16(*[data[11] << 8 | data[10]]),
                'dig_p4': self._read_signed16(*[data[13] << 8 | data[12]]),
                'dig_p5': self._read_signed16(*[data[15] << 8 | data[14]]),
                'dig_p6': self._read_signed16(*[data[17] << 8 | data[16]]),
                'dig_p7': self._read_signed16(*[data[19] << 8 | data[18]]),
                'dig_p8': self._read_signed16(*[data[21] << 8 | data[20]]),
                'dig_p9': self._read_signed16(*[data[23] << 8 | data[22]]),
                'dig_h1': self._read_signed8(*[data[24]]),
                'dig_h2': self._read_signed16(*[data[26] << 8 | data[25]]),
                'dig_h3': self._read_signed8(*[data[27]]),
                'dig_h4': self._read_signed16(*[data[28] << 4 | 0x0f & data[29]]),
                'dig_h5': self._read_signed16(*[data[30] << 4 | data[29] >> 4 & 0x0f]),
                'dig_h6': self._read_signed8(*[data[31]])
            })
        self._t_fine = 0

    def _read_signed16(self, value):
        if value >= 0x8000:
            value = (value - 0x10000)
        return value

    def _read_signed8(self, value):
        if value >= 0x80:
            value = (value - 0x100)
        return value

    def write(self, data):
        self.obniz.i2c0.write(*[self.address, data])

    async def get_data(self):
        self.i2c.write(*[self.address, [0xf7]])
        return await self.i2c.read_wait(*[self.address, 8])

    async def get_all_wait(self):
        data = await self.get_data()
        press_raw = data[0] << 12 | data[1] << 4 | data[2] >> 4
        temp_raw = data[3] << 12 | data[4] << 4 | data[5] >> 4
        hum_raw = data[6] << 8 | data[7]
        temperature = self.calibration_t(*[temp_raw]) / 100.0
        pressure = self.calibration_p(*[press_raw]) / 100.0
        humidity = self.calibration_h(*[hum_raw])
        return AttrDefault(bool, {'temperature': temperature, 'humidity': humidity, 'pressure': pressure})

    def calibration_t(self, adc_t):
        var1 = None
        var2 = None
        T = None
        var1 = (((adc_t >> 3) - (self._calibrated.dig_t1 << 1)) * self._calibrated.dig_t2) >> 11
        var2 = (((((adc_t >> 4) - self._calibrated.dig_t1) * ((adc_t >> 4) - self._calibrated.dig_t1)) >> 12) * self._calibrated.dig_t3) >> 14
        self._t_fine = (var1 + var2)
        T = (self._t_fine * 5 + 128) >> 8
        return T

    def calibration_p(self, adc_p):
        pvar1 = (self._t_fine / 2 - 64000)
        pvar2 = pvar1 * pvar1 * self._calibrated.dig_p6 / 32768
        pvar2 = (pvar2 + pvar1 * self._calibrated.dig_p5 * 2)
        pvar2 = (pvar2 / 4 + self._calibrated.dig_p4 * 65536)
        pvar1 = (self._calibrated.dig_p3 * pvar1 * pvar1 / 524288 + self._calibrated.dig_p2 * pvar1) / 524288
        pvar1 = (1 + pvar1 / 32768) * self._calibrated.dig_p1
        if pvar1 != 0:
            p = (1048576 - adc_p)
            p = (p - pvar2 / 4096) * 6250 / pvar1
            pvar1 = self._calibrated.dig_p9 * p * p / 2147483648
            pvar2 = p * self._calibrated.dig_p8 / 32768
            p = (p + ((pvar1 + pvar2) + self._calibrated.dig_p7) / 16)
            return p
        return 0

    def calibration_h(self, adc_h):
        h = (self._t_fine - 76800)
        h = (adc_h - (self._calibrated.dig_h4 * 64 + self._calibrated.dig_h5 / 16384 * h)) * self._calibrated.dig_h2 / 65536 * (1 + self._calibrated.dig_h6 / 67108864 * h * (1 + self._calibrated.dig_h3 / 67108864 * h))
        h = h * (1 - self._calibrated.dig_h1 * h / 524288)
        return h

    async def get_temp_wait(self):
        return await self.get_all_wait().temperature

    async def get_humd_wait(self):
        return await self.get_all_wait().humidity

    async def get_pressure_wait(self):
        return await self.get_all_wait().pressure

    async def get_altitude_wait(self):
        pressure = await self.get_pressure_wait()
        return self.calc_altitude(*[pressure])

    def calc_altitude(self, pressure, sea_level=1013.25):
        return (1.0 - math.pow(*[pressure / sea_level, 1 / 5.2553])) * 145366.45 * 0.3048