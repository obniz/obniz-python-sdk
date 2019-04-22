import asyncio
import json

from pyee import AsyncIOEventEmitter
import websockets

from .__version__ import __version__
from .libs.utils.util import ObnizUtil

class ObnizConnection:
    def __init__(self, id, options):
        self.id = id
        self.socket = None
        self.socket_local = None
        self.debugprint = False
        self.debugprint_binary = False
        self.bufferd_amound_warn_bytes = 10 * 1000 * 1000  # 10M bytes
        self.emitter = AsyncIOEventEmitter()

        self.onopen = None
        self.onconnect = None
        self.onclose = None
        self.on_connect_called = False
        self.send_pool = None
        self._sendQueueTimer = None
        self._wait_for_local_connect_ready_timer = None

        self._connection_retry_count = 0

        self._prepare_components()

        if options is None:
            options = {}

        self.options = {
            "auto_connect": options.get("auto_connect") is not False,
            "access_token": options.get("access_token"),
            "obniz_server": options.get("obniz_server", "wss://obniz.io"),
            "reset_obniz_on_ws_disconnection": options.get(
                "reset_obniz_on_ws_disconnection"
            )
            is not False,
        }

        if self.options["auto_connect"]:
            self.wsconnect()

    #   prompt(filled, callback) {
    #     obnizid = prompt('Please enter obniz id', filled)
    #     if (obnizid) {
    #       callback(obnizid)
    #     }
    #   }

    #   static get version() {
    #     packageJson = require('../package.json')
    #     return packageJson.version
    #   }

    def ws_on_open(self):
        self.print_debug("ws connected")
        self._connection_retry_count = 0
        if self.onopen is not None:
            self.onopen(self)

    def ws_on_message(self, data):
        obj = json.loads(data)

        if type(obj) is list:
            for o in obj:
                self.notify_to_module(o)
        else:
            # invalid json
            pass

    def ws_on_close(self):
        self.print_debug("closed")
        self.close()
        # self.emitter.emit('closed')
        if self.onclose and self.on_connect_called:
            self.onclose(self)

        self.on_connect_called = False

        self._reconnect()

    def connect_wait(self, callback, option={}):
        timeout = option.get("timeout")

        if self.on_connect_called:
            callback(True)
            return

        def cb(connected):
            nonlocal callback
            if callback:
                callback(connected)
            # 2回目以降の呼び出しではcallbackを呼ばない
            callback = None

        self.emitter.once("connected", lambda: cb(True))

        if not self.options["auto_connect"]:
            self.emitter.once("closed", lambda: cb(False))

        if timeout:
            asyncio.get_event_loop().call_later(timeout, lambda: cb(False))

        self.connect()

    def _reconnect(self):
        self._connection_retry_count += 1
        try_after = 1000
        if self._connection_retry_count > 15:
            try_after = (self._connection_retry_count - 15) * 1000
            limit = 60 * 1000
            if try_after > limit:
                try_after = limit

        if self.options["auto_connect"]:
            # setTimeout(() => {
            #     self.wsconnect() // always connect to mainserver if ws lost
            # }, tryAfter)
            pass

    #   wsOnError(event) {
    #     // console.error(event)
    #   }

    #   wsOnUnexpectedResponse(req, res) {
    #     if (res && res.statusCode == 404) {
    #       self.print_debug('obniz not online')
    #     } else {
    #       self.print_debug('invalid server response ' + res ? res.statusCode : '')
    #     }

    #     self.clearSocket(self.socket)
    #     delete self.socket

    #     self._reconnect()
    #   }

    def wsconnect(self, desired_server):
        server = self.options["obniz_server"]
        if desired_server:
            server = desired_server

        if self.socket and self.socket.open:
            self.close()

        url = server + "/obniz/{}/ws/1".format(self.id)

        query = ["obnizpy=" + __version__]
        if self.options["access_token"]:
            query.append("access_token=" + self.options["access_token"])
        url += "?" + "&".join(query)

        self.print_debug("connecting to " + url)

        async def connecting():
            async with websockets.connect(url) as websocket:
                self.socket = websocket
                self.ws_on_open()

                while True:
                    try:
                        data = await websocket.recv()
                        self.ws_on_message(data)
                    except websockets.exceptions.ConnectionClosed as e:
                        print(e)
                        self.ws_on_close()
                        break
                    except Exception as e:
                        print(e)
                        break

        asyncio.ensure_future(connecting())

    #   _connectLocal(host) {
    #     const url = 'ws://' + host
    #     self.print_debug('local connect to ' + url)
    #     ws
    #     if (self.isNode) {
    #       const wsClient = require('ws')
    #       ws = new wsClient(url)
    #       ws.on('open', () => {
    #         self.print_debug('connected to ' + url)
    #         self._callOnConnect()
    #       })
    #       ws.on('message', data => {
    #         self.print_debug('recvd via local')
    #         self.wsOnMessage(data)
    #       })
    #       ws.on('close', event => {
    #         console.log('local websocket closed')
    #         self._disconnectLocal()
    #       })
    #       ws.on('error', err => {
    #         console.error('local websocket error.', err)
    #         self._disconnectLocal()
    #       })
    #       ws.on('unexpected-response', event => {
    #         console.log('local websocket closed')
    #         self._disconnectLocal()
    #       })
    #     } else {
    #       ws = new WebSocket(url)
    #       ws.binaryType = 'arraybuffer'
    #       ws.onopen = () => {
    #         self.print_debug('connected to ' + url)
    #         self._callOnConnect()
    #       }
    #       ws.onmessage = event => {
    #         self.print_debug('recvd via local')
    #         self.wsOnMessage(event.data)
    #       }
    #       ws.onclose = event => {
    #         console.log('local websocket closed')
    #         self._disconnectLocal()
    #       }
    #       ws.onerror = err => {
    #         console.log('local websocket error.', err)
    #         self._disconnectLocal()
    #       }
    #     }
    #     self.socket_local = ws
    #   }

    def _disconnect_local(self):
        if self.socket_local:
            if self.socket.open:
                self.socket_local.close()

            self.clear_socket(self.socket_local)
            self.socket_local = None

        if self._wait_for_local_connect_ready_timer:
            # clearTimeout(self._wait_for_local_connect_ready_timer)
            self._wait_for_local_connect_ready_timer = None
            # should call. onlyl local connect was lost. and waiting.
            self._call_on_connect()

    def clear_socket(self, socket):
        if socket is None:
            return

        # send queue
        if self._sendQueueTimer:
            del self._sendQueue
            # clearTimeout(self._sendQueueTimer)
            self._sendQueueTimer = None

        # unbind
        # if (self.isNode) {
        #     shouldRemoveObservers = [
        #         'open',
        #         'message',
        #         'close',
        #         'error',
        #         'unexpected-response',
        #     ]
        #     for (i = 0 i < shouldRemoveObservers.length i++) {
        #         socket.removeAllListeners(shouldRemoveObservers[i])
        #     }
        # } else {
        #     socket.onopen = null
        #     socket.onmessage = null
        #     socket.onclose = null
        #     socket.onerror = null
        # }

    def connect(self):
        if self.socket and self.socket.open:
            return

        self.wsconnect()

    def close(self):
        # self._drainQueued()
        self._disconnect_local()
        if self.socket:
            if self.socket.open:
                #  Connecting & Connected
                self.socket.close(1000, "close")

            self.clear_socket(self.socket)
            self.socket = None

    def _call_on_connect(self):
        print("_call_on_connect")
        should_call = True
        if self._wait_for_local_connect_ready_timer:
            # obniz.js has wait local_connect
            # clearTimeout(self._wait_for_local_connect_ready_timer)
            self._wait_for_local_connect_ready_timer = None
        else:
            # obniz.js hasn't wait local_connect
            if self.socket_local and self.socket.open:
                # delayed connect
                should_call = False
            else:
                # local_connect is not used
                pass

        self.emitter.emit("connected")

        if should_call:
            if self.onconnect:
                try:
                    if asyncio.iscoroutinefunction(self.onconnect):
                        asyncio.ensure_future(self.onconnect(self))
                    else:
                        self.onconnect(self)
                except Exception as e:
                    print(e)

            self.on_connect_called = True

    def print_debug(self, str):
        if self.debugprint or self.debugprint_binary:
            print("Obniz: " + str)

    def send(self, obj, options=None):
        if obj is None:
            print("obnizpy. didnt send ", obj)
            return

        if type(obj) is list:
            for o in obj:
                self.send(o)
            return

        if self.send_pool is not None:
            self.send_pool.append(obj)
            return

        send_data = ObnizUtil.json_dumps([obj])
        if self.debugprint:
            self.print_debug("send: " + send_data)

        # queue sending
        # self._drainQueued()
        self._send_routed(send_data)

    def _send_routed(self, data):
        if self.socket_local and self.socket_local.on and type(data) is not str:
            self.print_debug("send via local")
            self.socket_local.send(data)
            if self.socket_local.buffered_amount > self.bufferd_amound_warn_bytes:
                self.warning(
                    "over " + self.socket_local.buffered_amount + " bytes queued"
                )
            return

        if self.socket and self.socket.open:
            asyncio.ensure_future(self.socket.send(data))
            # if self.socket.buffered_amount > self.bufferd_amound_warn_bytes:
            #     self.warning(
            #         f'over {self.socket.buffered_amount} bytes queued'
            #     )
            return

    # def _drainQueued(self):
    #     if self._sendQueue is None:
    #         return

    #     expect_size = 0
    #     for q in self._sendQueue:
    #         expect_size += q.length

    #     filled = 0
    #     # TODO: Uint8でなくていいかチェック
    #     # send_data = new Uint8Array(expectSize)
    #     send_data = [None] * expect_size
    #     for q in self._sendQueue:
    #         for i, d in enumerate(q):
    #             send_data[filled + i] = d
    #         filled += q.length

    #     self._send_routed(send_data)
    #     del self._sendQueue
    #     # clearTimeout(self._sendQueueTimer)
    #     # self._sendQueueTimer = null

    def _prepare_components(self):
        pass

    def notify_to_module(self, obj):
        if self.debugprint:
            self.print_debug(json.dumps(obj))

        if "ws" in obj:
            self.handle_ws_command(obj["ws"])
            return

        if "system" in obj:
            self.handle_system_command(obj["system"])
            return

    #   _canConnectToInsecure() {
    #     if (self.isNode) {
    #       return True
    #     } else {
    #       return location.protocol != 'https:'
    #     }
    #   }

    def handle_ws_command(self, ws_obj):
        if "ready" in ws_obj:
            self.firmware_ver = ws_obj["obniz"]["firmware"]
            if self.options["reset_obniz_on_ws_disconnection"]:
                self.reset_on_disconnect(True)

            # if (
            #     ws_obj.get('local_connect', {}).get('ip') and
            #     self.wscommand and
            #     self.options.local_connect and
            #     self._canConnectToInsecure()
            # ):
            #     self._connectLocal(ws_obj.local_connect.ip)
            #     # self._waitForLocalConnectReadyTimer = setTimeout(() => {
            #     #     self._callOnConnect()
            #     # }, 3000)
            # else:
            self._call_on_connect()

        if "redirect" in ws_obj:
            server = ws_obj["redirect"]
            self.print_debug("WS connection changed to " + server)

            # close current ws immidiately
            self.socket.close(1000, "close")
            self.clear_socket(self.socket)
            self.socket = None

            # connect to new server
            self.wsconnect(server)

    def handle_system_command(self, ws_obj):
        pass

    #   static get WSCommand() {
    #     return WSCommand
    #   }

    #   binary2Json(binary) {
    #     data = new Uint8Array(binary)
    #     json = []
    #     while (data !== null) {
    #       const frame = WSCommand.dequeueOne(data)
    #       if (!frame) break
    #       obj = {}
    #       for (i = 0 i < self.wscommands.length i++) {
    #         const command = self.wscommands[i]
    #         if (command.module === frame.module) {
    #           command.notifyFromBinary(obj, frame.func, frame.payload)
    #           break
    #         }
    #       }
    #       json.push(obj)
    #       data = frame.next
    #     }
    #     return json
    #   }

    def warning(self, msg):
        print("warning:" + str(msg))

    def error(self, msg):
        print("error:" + str(msg))
