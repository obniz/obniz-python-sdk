from .ble_attribute_abstract import BleAttributeAbstract


class BleRemoteAttributeAbstract(BleAttributeAbstract):
    def __init__(self, params):
        super().__init__(params)

        self.isRemote = False
        self.discoverdOnRemote = False

    @property
    def ws_child_uuid_name(self):
        children_name = self.children_name
        if not children_name:
            return None

        children_name = children_name[:-1]
        return children_name + "_uuid"

    def get_child(self, uuid):
        obj = super().get_child(uuid)
        if not obj:
            obj = self.add_child({"uuid": uuid})

        return obj

    # discoverChildren() {}

    # discoverChildrenWait() {
    #     return new Promise(resolve => {
    #         self.emitter.once('discoverfinished', () => {
    #             children = self.children.filter(elm => {
    #                 return elm.discoverdOnRemote
    #             })
    #             resolve(children)
    #         })
    #         self.discoverChildren()
    #     })
    # }

    #
    # CALLBACKS
    #
    def ondiscover(self):
        pass

    # ondiscoverfinished() {}

    def notify_from_server(self, notify_name, params):
        super().notify_from_server(notify_name, params)
        if notify_name == "discover":
            child = self.get_child(params[self.ws_child_uuid_name])
            child.discoverdOnRemote = True
            child.properties = params.get("properties", [])
            self.ondiscover(child)
        elif notify_name == "discoverfinished":
            children = [elm for elm in self.children if elm.discoverdOnRemote]
            self.ondiscoverfinished(children)
