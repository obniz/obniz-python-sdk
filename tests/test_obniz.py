from .utils import assert_finished, assert_send, receive_json


class TestObniz:
    def test_message(self, obniz):
        targets = ["1234-1231", "1234-1230"]

        obniz.message(targets, "pressed")

        assert_send(
            obniz, [{"message": {"data": "pressed", "to": ["1234-1231", "1234-1230"]}}]
        )
        assert_finished(obniz)

    def test_message_receive(self, obniz, mocker):
        obniz.onmessage = mocker.stub()

        receive_json(
            obniz, [{"message": {"data": "button pressed", "from": "1234-5678"}}]
        )

        assert obniz.onmessage.call_count == 1
        assert len(obniz.onmessage.call_args[0]) == 2
        assert obniz.onmessage.call_args[0][0] == "button pressed"
        assert obniz.onmessage.call_args[0][1] == "1234-5678"

    def test_message_receive2(self, obniz, mocker):
        obniz.onmessage = mocker.stub()

        receive_json(obniz, [{"message": {"data": [1, 2, 3, 4, 5, 10], "from": None}}])

        assert obniz.onmessage.call_count == 1
        assert len(obniz.onmessage.call_args[0]) == 2
        assert obniz.onmessage.call_args[0][0] == [1, 2, 3, 4, 5, 10]
        assert obniz.onmessage.call_args[0][1] is None

    def test_reset_on_disconnect(self, obniz):
        obniz.reset_on_disconnect(False)
        assert_send(obniz, [{"ws": {"reset_obniz_on_ws_disconnection": False}}])
        assert_finished(obniz)

    def test_ready(self, obniz, mocker):
        obniz.onconnect = mocker.stub()
        receive_json(obniz, [{"ws": {"ready": True, "obniz": {"firmware": "1.0.3"}}}])

        assert obniz.onconnect.call_count == 1
        assert len(obniz.onconnect.call_args[0]) == 1
        assert obniz.onconnect.call_args[0][0] == obniz

        assert_send(obniz, [{"ws": {"reset_obniz_on_ws_disconnection": True}}])

        assert_finished(obniz)

    def test_warning(self, obniz, mocker):
        obniz.warning = mocker.stub()
        receive_json(obniz, [{"debug": {"warning": {"message": "unknown command"}}}])

        assert obniz.warning.call_count == 1
        assert len(obniz.warning.call_args[0]) == 1
        assert obniz.warning.call_args[0][0] == {
            "alert": "warning",
            "message": "Warning: unknown command",
        }

        assert_finished(obniz)

    def test_error(self, obniz, mocker):
        error = obniz.error
        obniz.error = mocker.stub()
        receive_json(obniz, [{"debug": {"error": {"message": "voltage down"}}}])

        assert obniz.error.call_count == 1
        assert len(obniz.error.call_args[0]) == 1
        assert obniz.error.call_args[0][0] == {
            "alert": "error",
            "message": "Error: voltage down",
        }
        obniz.error = error

        assert_finished(obniz)
