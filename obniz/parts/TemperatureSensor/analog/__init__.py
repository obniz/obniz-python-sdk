import asyncio

class AnalogTemplatureSensor:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'output']
        self.required_keys = ['output']
        self.drive = '5v'
        self.onchange = None

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, self.drive])
        self.ad = obniz.get_ad(*[self.params.output])
        def calc_temp(voltage):
            self.temp = self.calc(voltage)
            if self.onchange:
                self.onchange(self.temp)
        self.ad.start(calc_temp)

    async def get_wait(self):
        voltage = await self.ad.get_wait()
        self.temp = self.calc(*[voltage])
        return self.temp

    def calc(self, voltage):
        return 0