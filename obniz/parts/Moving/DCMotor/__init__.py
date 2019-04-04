from attrdict import AttrDefault

class DCMotor:
    def __init__(self):
        self.keys = ['forward', 'back']
        self.required_keys = ['forward', 'back']

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'DCMotor'})

    def wired(self, obniz):
        self.status = AttrDefault(bool, {'direction': None, 'power': None})
        self.pwm1_io_num = self.params.forward
        self.pwm2_io_num = self.params.back
        self.pwm1 = obniz.get_free_pwm()
        self.pwm1.start(*[AttrDefault(bool, {'io': self.pwm1_io_num})])
        self.pwm1.freq(*[100000])
        self.pwm2 = obniz.get_free_pwm()
        self.pwm2.start(*[AttrDefault(bool, {'io': self.pwm2_io_num})])
        self.pwm2.freq(*[100000])
        self.power(*[30])

    def forward(self):
        self.move(*[True])

    def reverse(self):
        self.move(*[False])

    def stop(self):
        if self.status.direction == None:
            return
        self.status.direction = None
        self.pwm1.duty(*[0])
        self.pwm2.duty(*[0])

    def move(self, forward):
        if forward:
            if self.status.direction == True:
                return
            self.status.direction = True
        else:
            if self.status.direction == False:
                return
            self.status.direction = False
        power = self.power()
        self.power(*[0])
        self.power(*[power])

    def power(self, power=None):
        if power == None:
            return self.status.power
        self.status.power = power
        if self.status.direction == None:
            self.pwm1.duty(*[0])
            self.pwm2.duty(*[0])
            return
        if self.status.direction:
            self.pwm1.duty(*[power])
            self.pwm2.duty(*[0])
        else:
            self.pwm1.duty(*[0])
            self.pwm2.duty(*[power])