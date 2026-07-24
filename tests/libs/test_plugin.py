import asyncio

import pytest

from ..utils import (
    assert_finished,
    assert_send,
    receive_json,
    release_obnize,
    setup_obniz,
)


@pytest.fixture(scope="function")
def plugin_obniz(mocker):
    obniz = setup_obniz(mocker)
    receive_json(
        obniz,
        [{"ws": {"ready": True, "obniz": {"hw": "obnizb1", "firmware": "7.1.0"}}}],
    )
    assert_send(obniz, [{"ws": {"reset_obniz_on_ws_disconnection": True}}])

    yield obniz
    release_obnize(obniz)


@pytest.fixture(scope="function")
def old_firmware_obniz(mocker):
    obniz = setup_obniz(mocker)
    receive_json(
        obniz,
        [{"ws": {"ready": True, "obniz": {"hw": "obnizb1", "firmware": "3.0.0"}}}],
    )
    assert_send(obniz, [{"ws": {"reset_obniz_on_ws_disconnection": True}}])

    yield obniz
    release_obnize(obniz)


class TestPluginSend:
    def test_send_string(self, plugin_obniz):
        obniz = plugin_obniz
        obniz.plugin.send("obniz")

        assert_send(obniz, [{"plugin": {"send": [111, 98, 110, 105, 122]}}])
        assert_finished(obniz)

    def test_send_list(self, plugin_obniz):
        obniz = plugin_obniz
        obniz.plugin.send([0x00, 0x01, 0x02])

        assert_send(obniz, [{"plugin": {"send": [0, 1, 2]}}])
        assert_finished(obniz)

    def test_send_int(self, plugin_obniz):
        obniz = plugin_obniz
        obniz.plugin.send(0x10)

        assert_send(obniz, [{"plugin": {"send": [16]}}])
        assert_finished(obniz)

    def test_send_bytes(self, plugin_obniz):
        obniz = plugin_obniz
        obniz.plugin.send(b"\x10\x22\xf2")

        assert_send(obniz, [{"plugin": {"send": [16, 34, 242]}}])
        assert_finished(obniz)

    def test_send_requires_firmware_3_4_0(self, old_firmware_obniz):
        with pytest.raises(Exception, match="obniz firmware >= 3.4.0"):
            old_firmware_obniz.plugin.send([1])

        assert_finished(old_firmware_obniz)


class TestPluginReceive:
    def test_onreceive(self, mocker, plugin_obniz):
        obniz = plugin_obniz
        stub = mocker.stub()
        obniz.plugin.onreceive = stub

        receive_json(obniz, [{"plugin": {"receive": [111, 98, 110, 105, 122]}}])

        assert stub.call_count == 1
        assert stub.call_args[0][0] == [111, 98, 110, 105, 122]
        assert stub.call_args[0][1] == "obniz"
        assert_finished(obniz)

    def test_onreceive_binary_text_is_none(self, mocker, plugin_obniz):
        obniz = plugin_obniz
        stub = mocker.stub()
        obniz.plugin.onreceive = stub

        receive_json(obniz, [{"plugin": {"receive": [255, 254]}}])

        assert stub.call_args[0][0] == [255, 254]
        assert stub.call_args[0][1] is None
        assert_finished(obniz)

    def test_frame_callbacks(self, mocker, plugin_obniz):
        obniz = plugin_obniz
        on_start = mocker.stub()
        on_end = mocker.stub()
        obniz.plugin.onframestart = on_start
        obniz.plugin.onframeend = on_end

        receive_json(
            obniz, [{"plugin": {"frame": {"start": {"id": 100, "length": 10000}}}}]
        )
        receive_json(obniz, [{"plugin": {"frame": {"end": {"length": 500}}}}])

        assert on_start.call_args[0] == (100, 10000)
        assert on_end.call_count == 1
        assert_finished(obniz)

    def test_onerror(self, mocker, plugin_obniz):
        obniz = plugin_obniz
        stub = mocker.stub()
        obniz.plugin.onerror = stub

        receive_json(
            obniz, [{"plugin": {"error": {"message": "syntax error near 'x'"}}}]
        )

        assert stub.call_args[0][0] == {"message": "syntax error near 'x'"}
        assert_finished(obniz)


class TestPluginLua:
    def test_exec_lua(self, plugin_obniz):
        obniz = plugin_obniz
        obniz.plugin.exec_lua("duration = 60")

        assert_send(obniz, [{"plugin": {"exec_lua": "duration = 60"}}])
        assert_finished(obniz)

    def test_exec_lua_requires_string(self, plugin_obniz):
        with pytest.raises(Exception, match="must be a string"):
            plugin_obniz.plugin.exec_lua(123)

        assert_finished(plugin_obniz)

    def test_exec_lua_requires_firmware_7(self, old_firmware_obniz):
        with pytest.raises(Exception, match="obniz firmware >= 7.0.0"):
            old_firmware_obniz.plugin.exec_lua("duration = 60")

        assert_finished(old_firmware_obniz)

    def test_reload_lua(self, plugin_obniz):
        obniz = plugin_obniz
        obniz.plugin.reload_lua()

        assert_send(obniz, [{"plugin": {"reload": True}}])
        assert_finished(obniz)


class TestPluginCallWait:
    def test_call_wait_success(self, plugin_obniz):
        obniz = plugin_obniz
        loop = asyncio.get_event_loop()

        task = loop.create_task(obniz.plugin.call_wait("return 'hello'"))
        loop.run_until_complete(asyncio.sleep(0))

        assert_send(
            obniz,
            [{"plugin": {"call_request": {"id": 1, "lua": "return 'hello'"}}}],
        )

        receive_json(
            obniz,
            [{"plugin": {"call_response": {"id": 1, "status": 0, "result": "hello"}}}],
        )

        assert loop.run_until_complete(task) == "hello"
        assert_finished(obniz)

    def test_call_wait_lua_error(self, plugin_obniz):
        obniz = plugin_obniz
        loop = asyncio.get_event_loop()

        task = loop.create_task(obniz.plugin.call_wait("error('boom')"))
        loop.run_until_complete(asyncio.sleep(0))

        assert_send(
            obniz,
            [{"plugin": {"call_request": {"id": 1, "lua": "error('boom')"}}}],
        )

        receive_json(
            obniz,
            [{"plugin": {"call_response": {"id": 1, "status": 1, "result": "boom"}}}],
        )

        with pytest.raises(Exception, match="boom"):
            loop.run_until_complete(task)
        assert_finished(obniz)

    def test_call_wait_timeout(self, plugin_obniz):
        obniz = plugin_obniz
        loop = asyncio.get_event_loop()

        task = loop.create_task(
            obniz.plugin.call_wait("return 'never'", timeout=0.05)
        )
        loop.run_until_complete(asyncio.sleep(0.1))

        assert_send(
            obniz,
            [{"plugin": {"call_request": {"id": 1, "lua": "return 'never'"}}}],
        )

        with pytest.raises(Exception, match="timed out"):
            loop.run_until_complete(task)
        assert obniz.plugin._pending_calls == {}
        assert_finished(obniz)

    def test_call_wait_aborted_by_reset(self, plugin_obniz):
        obniz = plugin_obniz
        loop = asyncio.get_event_loop()

        task = loop.create_task(obniz.plugin.call_wait("return 1"))
        loop.run_until_complete(asyncio.sleep(0))

        assert_send(
            obniz, [{"plugin": {"call_request": {"id": 1, "lua": "return 1"}}}]
        )

        obniz.close()

        with pytest.raises(Exception, match="aborted by reset"):
            loop.run_until_complete(task)

    def test_call_wait_requires_firmware_7_1(self, old_firmware_obniz):
        loop = asyncio.get_event_loop()

        with pytest.raises(Exception, match="obniz firmware >= 7.1.0"):
            loop.run_until_complete(old_firmware_obniz.plugin.call_wait("return 1"))

        assert_finished(old_firmware_obniz)

    def test_transaction_id_increments(self, plugin_obniz):
        obniz = plugin_obniz
        loop = asyncio.get_event_loop()

        task1 = loop.create_task(obniz.plugin.call_wait("return 1"))
        task2 = loop.create_task(obniz.plugin.call_wait("return 2"))
        loop.run_until_complete(asyncio.sleep(0))

        assert_send(
            obniz, [{"plugin": {"call_request": {"id": 1, "lua": "return 1"}}}]
        )
        assert_send(
            obniz, [{"plugin": {"call_request": {"id": 2, "lua": "return 2"}}}]
        )

        receive_json(
            obniz,
            [{"plugin": {"call_response": {"id": 2, "status": 0, "result": "two"}}}],
        )
        receive_json(
            obniz,
            [{"plugin": {"call_response": {"id": 1, "status": 0, "result": "one"}}}],
        )

        assert loop.run_until_complete(task1) == "one"
        assert loop.run_until_complete(task2) == "two"
        assert_finished(obniz)


class TestPluginCloudTransaction:
    def test_sync_handler(self, plugin_obniz):
        obniz = plugin_obniz

        def handler(data, text):
            assert data == [111, 98, 110, 105, 122]
            assert text == "obniz"
            return "result for lua"

        obniz.plugin.oncloudtransaction = handler

        receive_json(
            obniz,
            [
                {
                    "plugin": {
                        "cloud_transaction_request": {
                            "id": 500,
                            "data": [111, 98, 110, 105, 122],
                        }
                    }
                }
            ],
        )

        assert_send(
            obniz,
            [
                {
                    "plugin": {
                        "cloud_transaction_response": {
                            "id": 500,
                            "success": True,
                            "result": "result for lua",
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_async_handler(self, plugin_obniz):
        obniz = plugin_obniz
        loop = asyncio.get_event_loop()

        async def handler(data, text):
            return [104, 105]  # "hi"

        obniz.plugin.oncloudtransaction = handler

        receive_json(
            obniz,
            [{"plugin": {"cloud_transaction_request": {"id": 1, "data": [1]}}}],
        )
        loop.run_until_complete(asyncio.sleep(0))

        assert_send(
            obniz,
            [
                {
                    "plugin": {
                        "cloud_transaction_response": {
                            "id": 1,
                            "success": True,
                            "result": "hi",
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_handler_exception_reports_failure(self, plugin_obniz):
        obniz = plugin_obniz

        def handler(data, text):
            raise Exception("handler broke")

        obniz.plugin.oncloudtransaction = handler

        receive_json(
            obniz,
            [{"plugin": {"cloud_transaction_request": {"id": 2, "data": [1]}}}],
        )

        assert_send(
            obniz,
            [
                {
                    "plugin": {
                        "cloud_transaction_response": {
                            "id": 2,
                            "success": False,
                            "result": "handler broke",
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_no_handler_reports_failure(self, plugin_obniz):
        obniz = plugin_obniz

        receive_json(
            obniz,
            [{"plugin": {"cloud_transaction_request": {"id": 3, "data": [1]}}}],
        )

        assert_send(
            obniz,
            [
                {
                    "plugin": {
                        "cloud_transaction_response": {
                            "id": 3,
                            "success": False,
                            "result": "no oncloudtransaction handler",
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)
