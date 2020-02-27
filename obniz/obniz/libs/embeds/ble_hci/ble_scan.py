from .ble_helper import BleHelper
from threading import Timer
from pyee import EventEmitter

class BleScan:
    ee = EventEmitter()
    def __init__(self, obnizBle):
        self.scan_target = None
        self.obnizBle = obnizBle

        self.scanned_peripherals = []

    def start(self, target=None, settings=None):
        if settings and 'duration' in settings:
            timeout = settings.duration
        else:
            timeout = 30
        
        self.scan_target = target

        if self.scan_target and "uuids" in self.scan_target and type(self.scan_target.uuids) is list:
            self.scan_target.uuids = [BleHelper.uuid_filter(e) for e in self.scan_target.uuids]
        self.scanned_peripherals = []

        self.obnizBle.central_bindings.start_scanning(None, False)

        timer = Timer(timeout, self.end)
        timer.start()

    ## def...

    def end(self):
        self.obnizBle.central_bindings.stop_scanning()

    def is_target(self, peripheral):
        if (self.scan_target
            and "local_name" in self.scan_target
            and peripheral.local_name is not self.scan_target.local_name):
            return False
        if self.scan_target and "uuids" in self.scan_target:
            uuids = [BleHelper.uuid_filter(e) for e in peripheral.advertisement_service_uuids()]
            for uuid in self.scan_target.uuids:
                if not uuid in uuids:
                    return False
        return True


    def onfinish(self, scanned_peripherals):
        pass

    def onfind(self, params):
        pass

    def notify_from_server(self, notify_name, params=None):
        if notify_name == 'onfind':
            # duplicate filter
            if next(filter(lambda e:e.address is params.address, self.scanned_peripherals), None):
                pass
            elif self.is_target(params):
                self.scanned_peripherals.append(params)
                self.ee.emit(notify_name, params)
                self.onfind(params)
        elif notify_name == 'onfinish':
            self.ee.emit(notify_name, self.scanned_peripherals)
            self.onfinish(self.scanned_peripherals)
