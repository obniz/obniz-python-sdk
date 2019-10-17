import asyncio
import time
from obniz import Obniz


# min 0.5 max 2.4 middle 1.4
async def onconnect(obniz):
    obniz.io0.output(False)
    obniz.io1.output(True)

    pwm = obniz.get_free_pwm()
    pwm.start({"io": 2})
    pwm.freq(100)
    pwm.duty(50)

    def read_state(state):
        print(state)
        if state == "right":
            val = 1.0
            pwm.pulse(val)
        elif state == "left":
            val = 1.8
            pwm.pulse(val)
        elif state == "none":
            val = 1.4
            pwm.pulse(val)

    obniz.switch.onchange = read_state


obniz = Obniz('15696177')
obniz.onconnect = onconnect

asyncio.get_event_loop().run_forever()