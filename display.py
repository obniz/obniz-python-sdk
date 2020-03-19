import asyncio
from obniz import Obniz

async def onconnect(obniz):
    obniz.display.clear()
    obniz.display.print("Hello, World!")

obniz = Obniz('54371148')
obniz.onconnect = onconnect

asyncio.get_event_loop().run_forever()