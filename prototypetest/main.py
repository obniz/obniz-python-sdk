
import asyncio
from obniz import Obniz

async def onconnect(obniz):
        print('connected')
        obniz.io0.output(False)
        obniz.io1.output(False)
        await obniz.wait(500)
        obniz.io1.output(True)
        await obniz.wait(500)
        obniz.io1.output(False)
        await obniz.wait(500)
        obniz.io1.output(True)
        await obniz.wait(500)
        obniz.io1.output(False)
        await obniz.wait(500)
        obniz.io1.output(True)
        await obniz.wait(500)
        obniz.io1.output(False)
        await obniz.wait(500)
        obniz.io1.output(True)
        await obniz.wait(500)
        obniz.io1.output(False)
        await obniz.wait(500)
        obniz.io1.output(True)

obniz = Obniz('98249879')
obniz.onconnect = onconnect

asyncio.get_event_loop().run_forever()


print(Obniz.obniz.version)


