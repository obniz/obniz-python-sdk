# from pyee import EventEmitter
from .ble_helper import BleHelper

class BleAttributeAbstract:
    def __init__(self, params):
        self.uuid = BleHelper.uuid_filter(params.uuid)
        self.parent = None
        self.children = []

        self.is_remote = False
        self.discoverd_on_remote = False

        self.data = params.data or None
        if not self.data and params.text:
            self.data = ObnizUtil.string2dataArray(params.text)

        if not self.data and params.value:
            self.data = [params.value]

        if params[self.childrenName]:
            for child in params[self.childrenName]:
                self.add_child(child)

    ## def...

    def add_child(self, child):
        print("wip: addChild")

    ## def...
