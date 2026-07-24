import asyncio

import pytest

from obniz.obniz.libs.hw.index import HW
from ...utils import (
    assert_finished,
    assert_send,
    receive_json,
    release_obnize,
    setup_obniz,
)


@pytest.fixture(scope="function")
def storage_obniz(mocker):
    # esp32c3 is a hw with the storage embed
    obniz = setup_obniz(mocker)
    receive_json(
        obniz,
        [{"ws": {"ready": True, "obniz": {"hw": "esp32c3", "firmware": "7.1.0"}}}],
    )
    assert_send(obniz, [{"ws": {"reset_obniz_on_ws_disconnection": True}}])

    yield obniz
    release_obnize(obniz)


class TestHwDefinitions:
    def test_new_hw_definitions_load(self):
        for hw in ["esp32c3", "esp32c6", "encored", "m5stickc", "blelte_gw2"]:
            assert HW.get_definition_for(hw) is not None

    def test_unknown_hw_returns_none(self):
        assert HW.get_definition_for("nosuchhw") is None
        assert HW.get_definition_for("../secret") is None
        assert HW.get_definition_for(None) is None


class TestStorageAttachment:
    def test_storage_attached_for_capable_hw(self, storage_obniz):
        assert hasattr(storage_obniz, "storage")
        assert "storage" in storage_obniz._all_component_keys

    def test_storage_not_attached_for_obnizb1(self, obniz):
        assert "storage" not in obniz._all_component_keys

    def test_plugin_always_attached(self, obniz, storage_obniz):
        assert "plugin" in obniz._all_component_keys
        assert "plugin" in storage_obniz._all_component_keys


class TestStorage:
    def test_save(self, storage_obniz):
        obniz = storage_obniz
        obniz.storage.save("launch_img", [1, 2, 3])

        assert_send(
            obniz,
            [{"storage": {"save": {"fileName": "launch_img", "data": [1, 2, 3]}}}],
        )
        assert_finished(obniz)

    def test_save_plugin_lua(self, storage_obniz):
        obniz = storage_obniz
        obniz.storage.save_plugin_lua('os.log("Hello")')

        expected = list('os.log("Hello")'.encode("utf-8"))
        assert_send(
            obniz, [{"storage": {"save": {"fileName": "plua", "data": expected}}}]
        )
        assert_finished(obniz)

    def test_save_plugin_lua_rejects_wrong_type(self, storage_obniz):
        with pytest.raises(Exception, match="no correct lua_script"):
            storage_obniz.storage.save_plugin_lua(123)

        assert_finished(storage_obniz)

    def test_read_wait(self, storage_obniz):
        obniz = storage_obniz
        loop = asyncio.get_event_loop()

        task = loop.create_task(obniz.storage.read_wait("plua"))
        loop.run_until_complete(asyncio.sleep(0))

        assert_send(obniz, [{"storage": {"read": {"fileName": "plua"}}}])

        receive_json(obniz, [{"storage": {"read": [10, 20, 30]}}])

        assert loop.run_until_complete(task) == [10, 20, 30]
        assert_finished(obniz)

    def test_reload_lua_after_save(self, storage_obniz):
        obniz = storage_obniz
        obniz.storage.save_plugin_lua('os.log("Hello")')
        obniz.plugin.reload_lua()

        expected = list('os.log("Hello")'.encode("utf-8"))
        assert_send(
            obniz, [{"storage": {"save": {"fileName": "plua", "data": expected}}}]
        )
        assert_send(obniz, [{"plugin": {"reload": True}}])
        assert_finished(obniz)
