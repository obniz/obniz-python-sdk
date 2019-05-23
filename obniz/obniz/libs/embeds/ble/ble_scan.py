from pyee import AsyncIOEventEmitter

from .ble_helper import BleHelper


class BleScan:
    def __init__(self, obniz):
        self.scan_target = None
        self.obniz = obniz
        self.emitter = AsyncIOEventEmitter()

        self.scaned_peripherals = []

    def start(self, target=None, settings=None):
        obj = {}
        obj["ble"] = {}
        obj["ble"]["scan"] = {
            #    "targetUuid" : settings and settings.targetUuid ? settings.targetUuid : None,
            #    "interval" : settings and settings.interval ? settings.interval : 30,
            "duration": settings["duration"]
            if settings and "duration" in settings
            else 30
        }

        self.scan_target = target
        if (
            self.scan_target
            and "uuids" in self.scan_target
            and type(self.scan_target["uuids"]) is list
        ):
            self.scan_target["uuids"] = [
                BleHelper.uuid_filter(elm) for elm in self.scan_target["uuids"]
            ]

        self.scaned_peripherals = []
        self.obniz.send(obj)

    #     startOneWait(target, settings) {
    #         state = 0

    #         return new Promise(resolve => {
    #             self.emitter.once('onfind', param => {
    #                 if (state === 0) {
    #                     state = 1
    #                     self.end()
    #                     resolve(param)
    #                 }
    #             })

    #             self.emitter.once('onfinish', () => {
    #                 if (state === 0) {
    #                     state = 1
    #                     resolve(None)
    #                 }
    #             })

    #             self.start(target, settings)
    #         })
    #     }

    #     startAllWait(target, settings) {
    #         return new Promise(resolve => {
    #             self.emitter.once('onfinish', () => {
    #                 resolve(self.scaned_peripherals)
    #             })

    #             self.start(target, settings)
    #         })
    #     }

    def end(self):
        obj = {}
        obj["ble"] = {}
        obj["ble"]["scan"] = None
        self.obniz.send(obj)

    def is_target(self, peripheral):
        if (
            self.scan_target
            and "local_name" in self.scan_target
            and peripheral.local_name != self.scan_target["local_name"]
        ):
            print("local")
            return False

        if self.scan_target and self.scan_target["uuids"]:
            uuids = [
                BleHelper.uuid_filter(e)
                for e in peripheral.advertisement_service_uuids()
            ]
            for uuid in self.scan_target["uuids"]:
                print("uuid = " + uuid + ", uuids = " + str(uuids))
                if uuid not in uuids:
                    print("not in")
                    return False

        return True

    def onfinish(self):
        pass  # dummy

    def onfind(self):
        pass  # dummy

    def notify_from_server(self, notify_name, params=None):
        print("notify_from_server")
        if notify_name == "onfind":
            print("onfind")
            if self.is_target(params):
                print("is target")
                self.scaned_peripherals.append(params)
                self.emitter.emit(notify_name, params)
                print("onfind")
                self.onfind(params)
        elif notify_name == "onfinish":
            self.emitter.emit(notify_name, self.scaned_peripherals)
            self.onfinish(self.scaned_peripherals)
