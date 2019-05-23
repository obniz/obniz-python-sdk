from attrdict import AttrDefault

class ServoMotor:
    def __init__(self):
        self.keys = ['gnd', 'vcc', 'signal', 'pwm']
        self.required_keys = []
        self.range = AttrDefault(bool, {'min': 0.5, 'max': 2.4})

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'ServoMotor'})

    def wired(self, obniz):
        self.obniz = obniz
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        if obniz.is_valid_io(*[self.params.vcc]):
            self.io_vcc = obniz.get_io(*[self.params.vcc])
        if self.params.pwm:
            self.pwm = self.params.pwm
        else:
            self.pwm = obniz.get_free_pwm()
            self.pwm_io_num = self.params.signal
            # self.pwm.start(*[AttrDefault(bool, {'io': self.pwm_io_num})])
            self.pwm.start({'io': self.pwm_io_num})
        self.pwm.freq(*[50])

    def angle(self, ratio):
        max = self.range.max
        min = self.range.min
        val = ((max - min) * ratio / 180.0 + min)
        self.pwm.pulse(*[val])

    def on(self):
        if self.io_vcc:
            self.io_vcc.output(*[True])

    def off(self):
        if self.io_vcc:
            self.io_vcc.output(*[False])