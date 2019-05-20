import math
from random import random
from time import time
import asyncio
from .obniz_components import ObnizComponents


class ObnizSystemMethods(ObnizComponents):
    def __init__(self, id, options):
        super().__init__(id, options)

    def wait(self, msec):
        if msec < 0:
            msec = 0
        elif msec > 60 * 1000:
            msec = 60 * 1000

        self.send({"system": {"wait": msec}})
        return asyncio.sleep(msec / 1000)

    def reset(self):
        self.send({"system": {"reset": True}})
        self._prepare_components()

    def reboot(self):
        self.send({"system": {"reboot": True}})
        self._prepare_components()

    def self_check(self):
        self.send({"system": {"self_check": True}})

    def keep_working_at_offline(self, working):
        self.send({"system": {"keep_working_at_offline": working}})

    def reset_on_disconnect(self, reset):
        self.send({"ws": {"reset_obniz_on_ws_disconnection": reset}})

    def ping_wait(self, unixtime=None, rand=None, force_global_network=None):
        unixtime = unixtime or int(time())
        upper = int(unixtime / math.pow(2, 32))
        lower = unixtime - upper * int(math.pow(2, 32))
        rand = rand or math.floor(random() * math.pow(2, 4))
        buf = []

        buf.append((upper >> (8 * 3)) & 0xFF)
        buf.append((upper >> (8 * 2)) & 0xFF)
        buf.append((upper >> (8 * 1)) & 0xFF)
        buf.append((upper >> (8 * 0)) & 0xFF)
        buf.append((lower >> (8 * 3)) & 0xFF)
        buf.append((lower >> (8 * 2)) & 0xFF)
        buf.append((lower >> (8 * 1)) & 0xFF)
        buf.append((lower >> (8 * 0)) & 0xFF)
        buf.append((rand >> (8 * 3)) & 0xFF)
        buf.append((rand >> (8 * 2)) & 0xFF)
        buf.append((rand >> (8 * 1)) & 0xFF)
        buf.append((rand >> (8 * 0)) & 0xFF)

        obj = {"system": {"ping": {"key": buf}}}

        self.send(obj, {"local_connect": not force_global_network})
        # get_running_loop() function is preferred on Python >= 3.7
        future = asyncio.get_event_loop().create_future()
        def cb(system_obj):
            for i, b in enumerate(buf):
                if b != system_obj["pong"]["key"][i]:
                    return

            # self.remove_pong_observer(cb)
            upper = (
                ((system_obj["pong"]["key"][0] << (8 * 3)) >> 0)
                + ((system_obj["pong"]["key"][1] << (8 * 2)) >> 0)
                + ((system_obj["pong"]["key"][2] << (8 * 1)) >> 0)
                + ((system_obj["pong"]["key"][3] << (8 * 0)) >> 0)
            )
            lower = (
                ((system_obj["pong"]["key"][4] << (8 * 3)) >> 0)
                + ((system_obj["pong"]["key"][5] << (8 * 2)) >> 0)
                + ((system_obj["pong"]["key"][6] << (8 * 1)) >> 0)
                + ((system_obj["pong"]["key"][7] << (8 * 0)) >> 0)
            )
            obniz_js_ping_unixtime = upper * math.pow(2, 32) + lower
            obniz_js_pong_unixtime = time()
            all_time = obniz_js_pong_unixtime - obniz_js_ping_unixtime
            time_js2server = (
                system_obj["pong"]["pingServerTime"] - obniz_js_ping_unixtime
            )
            time_server2obniz = (
                system_obj["pong"]["obnizTime"] - system_obj["pong"]["pingServerTime"]
            )
            time_obniz2server = (
                system_obj["pong"]["pongServerTime"] - system_obj["pong"]["obnizTime"]
            )
            time_server2js = (
                obniz_js_pong_unixtime - system_obj["pong"]["pongServerTime"]
            )
            string = (
                "ping " + str(all_time) + "ms (js --[" + str(time_js2server) + "ms]--> "
                + "server --[" + str(time_server2obniz) + "}ms]--> obniz --[" + str(time_obniz2server) + "}ms]--> "
                + "server --[" + str(time_server2js) + "}ms]--> js)"
            )

            self.print_debug(string)
            return string

        self.add_pong_observer(future, cb)
        return future
