from pyee import AsyncIOEventEmitter
import asyncio

from .ble_helper import BleHelper
from ...utils.util import ObnizUtil


class BleAttributeAbstract:
    def __init__(self, params):
        self.uuid = BleHelper.uuid_filter(params["uuid"])
        self.parent = None
        self.children = []

        self.isRemote = False
        self.discoverdOnRemote = False

        self.data = params.get("data")
        if not self.data and params.get("text"):
            self.data = ObnizUtil.string2data_array(params["text"])

        if not self.data and params.get("value"):
            self.data = [params.value]

        if self.children_name in params:
            for child in params[self.children_name]:
                self.add_child(child)

        self.set_functions()

        self.emitter = AsyncIOEventEmitter()

    def set_functions(self):
        children_name = self.children_name
        if children_name:
            child_name = children_name[:-1]

            func_name = "add_" + child_name
            setattr(self, func_name, self.add_child)

            func_name = "get_" + child_name
            setattr(self, func_name, self.get_child)

        parent_name = self.parent_name
        if parent_name:
            func_name = "get_" + parent_name
            setattr(self, func_name, self.get_parent)

            func_name = "set_" + parent_name
            setattr(self, func_name, self.set_parent)

    def get_parent(self):
        return self.parent

    def set_parent(self, new_value):
        self.parent = new_value

    @property
    def children_class(self):
        return object

    @property
    def children_name(self):
        return None

    @property
    def parent_name(self):
        return None

    def add_child(self, child):
        if not isinstance(child, self.children_class):
            children_class = self.children_class
            child = children_class(child)

        child.parent = self

        self.children.append(child)
        return child

    def get_child(self, uuid):
        uuid = BleHelper.uuid_filter(uuid)
        return next(
            iter(
                [
                    element
                    for element in self.children
                    if BleHelper.uuid_filter(element.uuid) == uuid
                ]
            ),
            None,
        )

    def to_json(self):
        obj = {"uuid": BleHelper.uuid_filter(self.uuid)}

        if len(self.children) > 0:
            key = self.children_name
            obj[key] = self.children

        if self.data:
            obj["data"] = self.data

        return obj

    # /**
    # * WS COMMANDS
    # */

    def read(self):
        pass

    def write(self):
        pass

    def write_number(self, val, need_response=False):
        self.write([val], need_response)

    # writeText(str, needResponse) {
    #     self.write(ObnizUtil.string2dataArray(str), needResponse)
    # }

    def read_wait(self):
        # get_running_loop() function is preferred on Python >= 3.7
        future = asyncio.get_event_loop().create_future()
        def cb(params):
            if params["result"] == "success":
                future.set_result(params["data"])
            else:
                future.set_result(None)
        self.emitter.once("onread", cb)
        self.read()
        return future

    # writeWait(data, needResponse) {
    #     return new Promise(resolve => {
    #         self.emitter.once('onwrite', params => {
    #             resolve(params.result == 'success')
    #         })
    #         self.write(data, needResponse)
    #     })
    # }

    # writeTextWait(data) {
    #     return new Promise(resolve => {
    #         self.emitter.once('onwrite', params => {
    #             resolve(params.result == 'success')
    #         })
    #         self.writeText(data)
    #     })
    # }

    # writeNumberWait(data) {
    #     return new Promise(resolve => {
    #         self.emitter.once('onwrite', params => {
    #             resolve(params.result == 'success')
    #         })
    #         self.writeNumber(data)
    #     })
    # }

    # readFromRemoteWait() {
    #     return new Promise(resolve => {
    #         self.emitter.once('onreadfromremote', () => {
    #             resolve()
    #         })
    #     })
    # }

    # writeFromRemoteWait() {
    #     return new Promise(resolve => {
    #         self.emitter.once('onreadfromremote', params => {
    #             resolve(params.data)
    #         })
    #     })
    # }

    #
    # CALLBACKS
    #
    def onwrite(self):
        pass

    def onread(self, data):
        pass

    def onwritefromremote(self):
        pass

    def onreadfromremote(self):
        pass

    def onerror(self, err):
        print(err.message)

    def notify_from_server(self, notify_name, params):
        self.emitter.emit(notify_name, params)
        if notify_name == "onerror":
            self.onerror(params)
        elif notify_name == "onwrite":
            self.onwrite(params["result"])
        elif notify_name == "onread":
            self.onread(params["data"])
        elif notify_name == "onwritefromremote":
            self.onwritefromremote(params["address"], params["data"])
        elif notify_name == "onreadfromremote":
            self.onreadfromremote(params["address"])
