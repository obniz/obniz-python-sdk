import semver

from ..utils.eventloop import get_event_loop


class Storage:
    def __init__(self, obniz):
        self.obniz = obniz
        self._read_futures = []

    def _reset(self):
        for future in self._read_futures:
            if not future.done():
                future.set_exception(
                    Exception("obniz.storage.read_wait() aborted by reset")
                )
        self._read_futures = []

    def save(self, file_name, data):
        self._require_firmware_major(4)

        if isinstance(data, (bytes, bytearray)):
            data = list(data)
        if type(data) is not list:
            raise Exception("storage save data must be a list of bytes")

        self.obniz.send(
            {"storage": {"save": {"fileName": file_name, "data": data}}}
        )

    def save_plugin_lua(self, lua_script):
        self._require_firmware_major(7)

        if type(lua_script) is str:
            send_data = list(lua_script.encode("utf-8"))
        elif isinstance(lua_script, (bytes, bytearray)):
            send_data = list(lua_script)
        elif type(lua_script) is list:
            send_data = lua_script
        else:
            raise Exception("no correct lua_script supplied")

        self.save("plua", send_data)

    async def read_wait(self, file_name):
        future = get_event_loop().create_future()
        self._read_futures.append(future)

        self.obniz.send({"storage": {"read": {"fileName": file_name}}})

        try:
            return await future
        finally:
            if future in self._read_futures:
                self._read_futures.remove(future)

    def notified(self, obj):
        if "read" in obj:
            for future in self._read_futures:
                if not future.done():
                    future.set_result(obj["read"])
                    break

    def _require_firmware_major(self, major):
        fw = self.obniz.firmware_ver
        if not fw:
            raise Exception("unknown obniz firmware version. connect first")

        if semver.Version.parse(fw).major < major:
            raise Exception(
                "Please update obniz firmware >= {}.0.0".format(major)
            )
