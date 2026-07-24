import asyncio

from .utils import assert_finished, assert_send, receive_json


class TestMessage:
    def test_message_to_string_target(self, obniz):
        obniz.message("12345678", "button pressed")

        assert_send(
            obniz, [{"message": {"to": ["12345678"], "data": "button pressed"}}]
        )
        assert_finished(obniz)

    def test_message_to_list_target(self, obniz):
        obniz.message(["12345678", "87654321"], "button pressed")

        assert_send(
            obniz,
            [{"message": {"to": ["12345678", "87654321"], "data": "button pressed"}}],
        )
        assert_finished(obniz)


class TestOndebug:
    def test_ondebug_called_with_dict(self, mocker, obniz):
        stub = mocker.stub()
        obniz.ondebug = stub

        receive_json(
            obniz, [{"debug": {"warning": {"message": "unknown command"}}}]
        )

        assert stub.call_count == 1
        assert stub.call_args[0][0] == {"warning": {"message": "unknown command"}}


class TestLogicAnalyzerMeasured:
    def test_measured_accumulates_without_onmeasured(self, obniz):
        obniz.logicAnalyzer.start({"io": 1, "interval": 0.1, "duration": 100})
        assert_send(
            obniz, [{"logic_analyzer": {"interval": 0.1, "io": [1], "duration": 100}}]
        )

        data1 = [0, 1] * 100
        data2 = [1, 0] * 100
        receive_json(obniz, [{"logic_analyzer": {"data": data1}}])
        receive_json(obniz, [{"logic_analyzer": {"data": data2}}])

        assert obniz.logicAnalyzer.measured == [data1, data2]
        assert_finished(obniz)


class TestClose:
    def test_close_awaits_socket_close(self, obniz):
        socket = obniz.socket
        obniz.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.sleep(0))

        socket.close.assert_awaited_once_with(1000, "close")
        assert obniz.socket is None
        assert obniz.connection_state == "closed"


class TestRepeat:
    def test_repeat_with_sync_callback(self, obniz):
        calls = []
        obniz.repeat(lambda: calls.append(1), interval=10)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.sleep(0.05))
        obniz.looper = None

        assert len(calls) >= 2

    def test_repeat_with_async_callback(self, obniz):
        calls = []

        async def looper():
            calls.append(1)

        obniz.repeat(looper, interval=10)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.sleep(0.05))
        obniz.looper = None

        assert len(calls) >= 2
