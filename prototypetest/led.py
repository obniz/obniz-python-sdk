
import asyncio
from obniz import Obniz

async def onconnect(obniz):
        print('connected')
        led = obniz.wired('LED',{ "anode":0, "cathode":1})
        led.on()
        await obniz.wait(500)
        led.off()
        await obniz.wait(500)
        led.on()
        await obniz.wait(500)
        led.off()
        await obniz.wait(500)
        led.on()
        await obniz.wait(500)
        led.off()
        await obniz.wait(500)

obniz = Obniz('15696177')
obniz.debugprint = True
obniz.onconnect = onconnect

asyncio.get_event_loop().run_forever()


print(Obniz.obniz.version)


