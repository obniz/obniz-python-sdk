import asyncio
from obniz import Obniz

async def onconnect(obniz):
    obniz.display.clear()
    obniz.display.print("Hello, World!")

obniz = Obniz('15696177')
obniz.onconnect = onconnect

asyncio.get_event_loop().run_forever()