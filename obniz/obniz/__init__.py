import asyncio

from .obniz_uis import ObnizUIs

name = "obniz"

class Obniz(ObnizUIs):
    def __init__(self, id, options=None):
        super().__init__(id, options)

        self.looper = None
        self.ondebug = None


    def repeat(self, callback, interval=100):
        if self.looper:
            self.looper = callback
            return

        self.looper = callback
        self.repeatInterval = interval

        if self.on_connect_called:
            self.loop()

    def _call_on_connect(self):
        super()._call_on_connect()
        self.loop()

    def loop(self):
        if self.looper:
            prom = self.looper()
            if prom:
                prom()

            asyncio.get_event_loop().call_later(1, self.loop)

    def ws_on_close(self):
        super().ws_on_close()
        if self.looper:
            self.looper = None

    def message(self, target, message):
        targets = []
        if type(target) is str:
            targets.push(target)
        else:
            targets = target

        self.send({"message": {"to": targets, "data": message}})

    def notify_to_module(self, obj):
        super().notify_to_module(obj)
        # notify messaging
        if "message" in obj and self.onmessage:
            self.onmessage(obj["message"]["data"], obj["message"]["from"])

        # debug
        if "debug" in obj:
            if "warning" in obj["debug"]:
                msg = "Warning: " + obj["debug"]["warning"]["message"]
                self.warning({"alert": "warning", "message": msg})

            if "error" in obj["debug"]:
                msg = "Error: " + obj["debug"]["error"]["message"]
                self.error({"alert": "error", "message": msg})

            if self.ondebug:
                self.ondebug(obj.debug)

#######################
# ReadParts
#######################
import os
import glob
import pathlib
import importlib

# Get current working directory path
basepath = pathlib.Path(__file__).parent.resolve()
# Get parts library path
libpath = pathlib.Path(str(basepath) + "/../parts").resolve()
# Get ALL parts class path
cls_paths = glob.glob(str(libpath) + "/*")
for cls_path in cls_paths:
    parts_cls = pathlib.Path(cls_path).name
    # Get ALL parts path (including __init__.py)
    parts = glob.glob(cls_path + "/**/__init__.py", recursive=True)
    for part in parts:
        partpath = pathlib.Path(part).resolve().parent
        part_name = partpath.name.replace("-", "")
        # Import parts module
        module_path = "obniz" + str(partpath).replace(str(basepath.parent), "").replace(os.sep, ".")
        module = importlib.import_module(module_path)
        try:
            if "info" in dir(getattr(module, part_name)):
                # Registrate
                Obniz.parts_registrate(getattr(module, part_name)())
        except AttributeError as e:
            pass
