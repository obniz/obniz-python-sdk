from attrdict import AttrDefault

import asyncio

import math

class HCSR04:
    def __init__(self):
        self.keys = ['vcc', 'trigger', 'echo', 'gnd']
        self.required_keys = ['vcc', 'trigger', 'echo']
        self._unit = 'mm'
        self.reset_alltime = False
        self.temp = 15
        self.onchange = None

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'HC-SR04'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[None, self.params.gnd, '5v'])
        self.vcc_io = obniz.get_io(*[self.params.vcc])
        self.trigger = self.params.trigger
        self.echo = self.params.echo
        self.vcc_io.drive(*['5v'])
        self.vcc_io.output(*[True])
        self.obniz.wait(*[100])

    def measure(self, callback=None, future=None):
        def anonym_func(edges):
            if self.reset_alltime:
                self.vcc_io.output(False)
                self.obniz.wait(100)
                self.vcc_io.output(True)
                self.obniz.wait(100)
            distance = None
            for i in range(0, len(edges) - 1):
                # HCSR04's output of io_echo is initially high when trigger is finshed
                if (edges[i]["edge"] is True):
                    time = (edges[i + 1]["timing"] - edges[i]["timing"]) / 1000 # (1/4000 * 8) + is needed??
                    distance = (time / 2) * 20.055 * math.sqrt(self.temp + 273.15) * 1000
                    if self.unit == "inch":
                        distance = distance * 0.0393701
            if callable(callback):
                callback(distance)
            if future:
                future.set_result(distance)

        self.obniz.measure.echo(
            *[AttrDefault(bool, 
                {
                    'io_pulse': self.trigger,
                    'io_echo': self.echo,
                    'pulse': 'positive',
                    'pulse_width': 0.011,
                    'measure_edges': 3,
                    'timeout': 10 / 340 * 1000,
                    'callback': anonym_func
                }
            )]
        )

    def measure_wait(self):
        # get_running_loop() function is preferred on Python >= 3.7
        future = asyncio.get_event_loop().create_future()
        self.measure(future=future)
        return future

    def unit(self, unit):
        if unit == 'mm':
            self._unit = 'mm'
        elif unit == 'inch':
            self._unit = 'inch'
        else:
            raise Exception('HCSR04: unknown unit ' + str(unit))