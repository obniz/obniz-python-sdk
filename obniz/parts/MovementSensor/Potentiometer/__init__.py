from attrdict import AttrDefault

class Potentiometer:
    def __init__(self):
        self.keys = ['pin0', 'pin1', 'pin2']
        self.required_keys = ['pin0', 'pin1', 'pin2']
        self.vcc_voltage = 5.0

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'Potentiometer'})

    def wired(self, obniz):
        self.obniz.set_vcc_gnd(*[self.params.pin0, self.params.pin2, '5v'])
        self.ad = obniz.get_ad(*[self.params.pin1])

        def set_voltage(value):
            self.vcc_voltage = value
        obniz.get_ad(*[self.params.pin0]).start(set_voltage)

        def set_position(value):
            self.position = value / self.vcc_voltage
            if self.onchange:
                self.onchange(self.position)
        self.ad.start(set_position)