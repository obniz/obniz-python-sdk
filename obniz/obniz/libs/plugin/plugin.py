import asyncio
import inspect

import semver

from ..utils.eventloop import ensure_future, get_event_loop


class Plugin:
    def __init__(self, obniz):
        self.obniz = obniz

        # onreceive(data, text) is called when plugin data arrives.
        # text is the utf-8 decoded form of data, or None if not decodable.
        self.onreceive = None
        # onframestart(frame_id, length) / onframeend()
        self.onframestart = None
        self.onframeend = None
        # onerror(error) receives {"message": ...} e.g. Lua syntax errors
        self.onerror = None
        # oncloudtransaction(data, text) handles cloud.transactionWait()
        # from Lua on the device. May be a plain function or a coroutine
        # function. Its return value is sent back to the waiting Lua code;
        # raising reports failure instead.
        self.oncloudtransaction = None

        self._call_transaction_id = 0
        self._pending_calls = {}

    def _reset(self):
        for future in self._pending_calls.values():
            if not future.done():
                future.set_exception(
                    Exception("obniz.plugin.call_wait() aborted by reset")
                )
        self._pending_calls = {}

    def send(self, data):
        self._require_firmware("3.4.0")

        if data is None:
            return
        if type(data) is int:
            data = [data]

        if isinstance(data, (bytes, bytearray)):
            send_data = list(data)
        elif type(data) is list:
            send_data = data
        elif type(data) is str:
            send_data = list(data.encode("utf-8"))
        else:
            raise Exception("plugin send accepts str, int, list or bytes")

        self.obniz.send({"plugin": {"send": send_data}})

    def exec_lua(self, lua_script):
        self._require_firmware("7.0.0")

        if type(lua_script) is not str:
            raise Exception("Lua Script must be a string")

        self.obniz.send({"plugin": {"exec_lua": lua_script}})

    def reload_lua(self):
        self._require_firmware("7.0.0")

        self.obniz.send({"plugin": {"reload": True}})

    async def call_wait(self, lua_script, timeout=30):
        self._require_firmware("7.1.0")

        if type(lua_script) is not str:
            raise Exception("Lua Script must be a string")

        id = self._get_next_transaction_id()
        future = get_event_loop().create_future()
        self._pending_calls[id] = future

        self.obniz.send({"plugin": {"call_request": {"id": id, "lua": lua_script}}})

        try:
            if timeout and timeout > 0:
                try:
                    return await asyncio.wait_for(future, timeout)
                except asyncio.TimeoutError:
                    raise Exception("obniz.plugin.call_wait() timed out")
            return await future
        finally:
            self._pending_calls.pop(id, None)

    def notified(self, obj):
        if "receive" in obj:
            data = obj["receive"]
            if self.onreceive:
                self.onreceive(data, self._data_to_string(data))
        elif "frame" in obj:
            frame = obj["frame"]
            if "start" in frame:
                if self.onframestart:
                    self.onframestart(
                        frame["start"].get("id"), frame["start"]["length"]
                    )
            elif "end" in frame:
                if self.onframeend:
                    self.onframeend()
        elif "error" in obj:
            if self.onerror:
                self.onerror(obj["error"])
        elif "call_response" in obj:
            self._on_call_response(obj["call_response"])
        elif "cloud_transaction_request" in obj:
            self._handle_cloud_transaction(obj["cloud_transaction_request"])

    def _require_firmware(self, version):
        fw = self.obniz.firmware_ver
        if not fw:
            raise Exception("unknown obniz firmware version. connect first")

        info = semver.parse_version_info(fw)
        if version == "7.1.0":
            # accept prereleases like 7.1.0-beta.0, as obniz.js does
            ok = info.major > 7 or (info.major == 7 and info.minor >= 1)
        elif version == "7.0.0":
            ok = info.major >= 7
        else:
            ok = not semver.match(fw, "<" + version)

        if not ok:
            raise Exception("Please update obniz firmware >= " + version)

    def _get_next_transaction_id(self):
        self._call_transaction_id = (self._call_transaction_id + 1) & 0xFFFFFFFF
        if self._call_transaction_id == 0:
            self._call_transaction_id = 1
        return self._call_transaction_id

    def _on_call_response(self, res):
        future = self._pending_calls.get(res["id"])
        if future is None or future.done():
            return
        if res.get("status") == 0:
            future.set_result(res.get("result", ""))
        else:
            future.set_exception(Exception(res.get("result") or "Lua error"))

    def _handle_cloud_transaction(self, req):
        id = req["id"]
        data = req["data"]

        if self.oncloudtransaction is None:
            # report failure so Lua does not hang until its own timeout
            self._send_cloud_transaction_response(
                id, False, "no oncloudtransaction handler"
            )
            return

        try:
            ret = self.oncloudtransaction(data, self._data_to_string(data) or "")
        except Exception as e:
            self._send_cloud_transaction_response(id, False, str(e))
            return

        if inspect.isawaitable(ret):
            async def _wait_handler():
                try:
                    result = self._transaction_result_to_string(await ret)
                except Exception as e:
                    self._send_cloud_transaction_response(id, False, str(e))
                else:
                    self._send_cloud_transaction_response(id, True, result)

            ensure_future(_wait_handler())
        else:
            self._send_cloud_transaction_response(
                id, True, self._transaction_result_to_string(ret)
            )

    def _send_cloud_transaction_response(self, id, success, result):
        self.obniz.send(
            {
                "plugin": {
                    "cloud_transaction_response": {
                        "id": id,
                        "success": success,
                        "result": result,
                    }
                }
            }
        )

    @staticmethod
    def _data_to_string(data):
        try:
            return bytes(data).decode("utf-8")
        except (UnicodeDecodeError, ValueError):
            return None

    @staticmethod
    def _transaction_result_to_string(ret):
        if ret is None:
            return ""
        if type(ret) is str:
            return ret
        if isinstance(ret, (bytes, bytearray)):
            return bytes(ret).decode("utf-8")
        if type(ret) is list:
            return bytes(ret).decode("utf-8")
        return str(ret)
