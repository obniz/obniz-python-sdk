import asyncio
import builtins
import json
import time

from .obniz_json_validator import obniz_json_validator as validator
from .utils import (
    assert_finished,
    assert_obniz,
    create_obniz,
    create_server,
    receive_json,
)

wait_ms = 50


class TestInit:
    def test_instance(self, mocker):
        mocker.spy(builtins, "print")
        obniz = create_obniz(3000, "OBNIZ_ID_HERE")

        assert_obniz(obniz)
        assert builtins.print.call_count == 1
        assert builtins.print.call_args[0][0] == "error:invalid obniz id"

    def test_connect(self):
        port = 8080  # getPort()

        loop = asyncio.get_event_loop()
        future = loop.create_future()

        async def on_connection(websocket, path):
            print("server: connected")

            future.set_result(None)

        server = create_server(port, on_connection)
        obniz = create_obniz(port, "11111111")

        loop.run_until_complete(future)

        self._wait(wait_ms)

        assert_obniz(obniz)

        obniz.close()
        server.close()

    def test_soft_redirect(self):
        port = 8080
        port2 = 8081
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        async def on_connection(websocket, path):
            try:
                print("server(" + str(port) + "): connected")
                future.set_result(websocket)

                await websocket.recv()
            except Exception as e:
                future.set_exception(e)

        print("create_server(" + str(port) + ")")
        server = create_server(port, on_connection)
        print("create_obniz")
        obniz = create_obniz(port, "11111111")
        obniz.debugprint = True

        assert_obniz(obniz)

        print("wait future")
        websocket = loop.run_until_complete(future)
        print("done future")

        self._wait(wait_ms)

        # expect(server.clients.size, 'before server not connected').to.equal(1)
        future2 = loop.create_future()

        async def on_connection2(websocket, path):
            try:
                print("server(" + str(port2) + "): connected")
                future2.set_result(None)

                await websocket.recv()
            except Exception as e:
                future2.set_exception(e)

        print("create_server(" + str(port2) + ")")
        server2 = create_server(port2, on_connection2)

        val = [{"ws": {"redirect": "ws://localhost:" + str(port2)}}]

        results = validator.response_validate(val, "json")
        assert results["valid"], results["errors"]

        print("send redirect signal")
        loop.run_until_complete(websocket.send(json.dumps(val)))

        print("wait future2")
        loop.run_until_complete(future2)
        print("done future2")

        self._wait(wait_ms)

        # expect(server.clients.size, 'before server remain connection').to.equal(0)
        # expect(server2.clients.size, 'after server not connected').to.equal(1)
        obniz.close()
        server.close()
        server2.close()

    def test_onconnect(self, obniz):
        called = False

        assert_obniz(obniz)
        assert_finished(obniz)  # input queue

        def onconnect(obniz):
            nonlocal called
            called = True

        obniz.onconnect = onconnect

        receive_json(obniz, [{"ws": {"ready": True, "obniz": {"firmware": "1.0.3"}}}])

        self._wait(500)

        assert called

    def test_repeat(self, obniz):
        called = False
        assert_obniz
        assert_finished  # input queue

        def callback():
            nonlocal called
            called = True

        obniz.repeat(callback)
        receive_json(obniz, [{"ws": {"ready": True, "obniz": {"firmware": "1.0.3"}}}])

        self._wait(500)
        obniz.looper = None

        assert called is True

    def test_connect_repeat(self, obniz):
        results = True
        assert_obniz
        assert_finished  # input queue

        called = False

        def onconnect(obniz):
            nonlocal results, called
            results = results and called is False
            called = True

        obniz.onconnect = onconnect

        def callback():
            nonlocal results, called
            results = results and called is True
            called = True

        obniz.repeat(callback)

        receive_json(obniz, [{"ws": {"ready": True, "obniz": {"firmware": "1.0.3"}}}])

        self._wait(500)
        obniz.looper = None
        assert results is True

    def test_connect_wait(self, obniz):
        called = False
        assert_obniz
        assert_finished  # input queue

        def callback(connected):
            nonlocal called
            called = connected is True

        obniz.connect_wait(callback)

        receive_json(obniz, [{"ws": {"ready": True, "obniz": {"firmware": "1.0.3"}}}])

        self._wait(500)
        assert called is True

    def test_connect_wait_timeout(self, obniz):
        called = False
        assert_obniz
        assert_finished  # input queue

        def callback(connected):
            nonlocal called
            called = connected is False

        obniz.connect_wait(callback, {"timeout": 1})

        def timer(loop):
            try:
                receive_json(
                    obniz, [{"ws": {"ready": True, "obniz": {"firmware": "1.0.3"}}}]
                )
            except Exception as e:
                print(e)
            finally:
                loop.stop()

        loop = asyncio.get_event_loop()
        loop.call_later(1.5, timer, loop)
        loop.run_forever()
        # loop.close()
        assert called is True

    def _wait(self, ms):
        time.sleep(ms / 1000)
