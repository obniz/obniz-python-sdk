
import asyncio
from obniz import Obniz

async def onconnect(obniz):
        print('connected')
        obniz.io1.output(False)
        obniz.io0.output(False)
        await obniz.wait(500)
        obniz.io0.output(True)
        await obniz.wait(500)
        obniz.io0.output(False)
        await obniz.wait(500)
        obniz.io0.output(True)
        await obniz.wait(500)
        obniz.io0.output(False)
        await obniz.wait(500)
        obniz.io0.output(True)
        await obniz.wait(500)
        obniz.io0.output(False)
        await obniz.wait(500)
        obniz.io0.output(True)
        await obniz.wait(500)
        obniz.io0.output(False)
        await obniz.wait(500)
        obniz.io0.output(True)

obniz = Obniz('15696177')
obniz.onconnect = onconnect

asyncio.get_event_loop().run_forever()


print(Obniz.obniz.version)


