from functools import partial

class LED:
    def __init__(self):
        self.keys = ['anode', 'cathode']
        self.required_keys = ['anode']

    @staticmethod
    def info():
        return { "name": "LED" }
    
    def wired(self, obniz):
        self.obniz = obniz
        self.io_anode = obniz.get_io(self.params["anode"])
        self.io_anode.output(False)
        if "cathode" in self.params:
            self.io_cathode = obniz.get_io(self.params["cathode"])
            self.io_cathode.output(False)
        self.animation_name = 'Led-' + str(self.params["anode"])
    
    def on(self):
        self.end_blink()
        self.io_anode.output(True)
    
    def off(self):
        self.end_blink()
        self.io_anode.output(False)
    
    def output(self, value):
        if value:
            self.on()
        else:
            self.off()
    
    def end_blink(self):
        self.obniz.io.animation(self.animation_name, 'pause')
    
    def blink(self, interval=100):
        frames = [
            {
                "duration": interval,
                "state": partial(lambda index: self.io_anode.output(True))
            },
            {
                "duration": interval,
                "state": partial(lambda index: self.io_anode.output(False))
            }
        ]

        self.obniz.io.animation(self.animation_name, 'loop', frames)
