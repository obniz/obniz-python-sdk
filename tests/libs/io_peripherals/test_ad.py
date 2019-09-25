from time import sleep

import pytest

from ...utils import assert_finished, assert_obniz, assert_send, receive_json


class TestPeripheralAD:
    def test_get_ad(self, obniz):
        ad0 = obniz.get_ad(0)
        assert ad0.id == 0

        ad11 = obniz.get_ad(11)
        assert ad11.id == 11

        with pytest.raises(Exception, match="ad 12 is not valid io"):
            obniz.get_ad(12)

        with pytest.raises(Exception, match="ad 0 is not valid io"):
            obniz.get_ad("0")

        assert_finished(obniz)

    def test_start(self, mocker, obniz):
        stub = mocker.stub()
        obniz.ad0.start(stub)

        assert_send(obniz, [{"ad0": {"stream": True}}])
        assert_finished(obniz)

    def test_value(self, mocker, obniz):
        stub = mocker.stub()
        obniz.ad0.start(stub)
        assert_send(obniz, [{"ad0": {"stream": True}}])

        receive_json(obniz, [{"ad0": 0}])
        assert stub.call_count == 1
        assert stub.call_args[0][0] == 0

        receive_json(obniz, [{"ad0": 4.9}])
        assert stub.call_count == 2
        assert stub.call_args[0][0] == 4.9

        assert_finished(obniz)

    def test_onchange(self, mocker, obniz):
        stub = mocker.stub()
        obniz.ad1.start()
        obniz.ad1.onchange = stub
        assert_send(obniz, [{"ad1": {"stream": True}}])

        receive_json(obniz, [{"ad1": 0}])
        assert stub.call_count == 1
        assert stub.call_args[0][0] == 0

        receive_json(obniz, [{"ad0": 4.9}])
        assert stub.call_count == 1

        assert_finished(obniz)

    def test_in_var(self, obniz):
        obniz.ad1.start()
        assert_send(obniz, [{"ad1": {"stream": True}}])

        receive_json(obniz, [{"ad1": 1}])
        assert obniz.ad1.value == 1

        assert_finished(obniz)

    def test_input_wait_true(self, obniz):
        def callback(result):
            assert result == 2.6

        obniz.ad4.get_wait().add_done_callback(callback)

        assert_obniz(obniz)
        assert_send(obniz, [{"ad4": {"stream": False}}])
        assert_finished(obniz)

        sleep(0.01)
        receive_json(obniz, [{"ad4": 2.6}])

    def test_end(self, obniz):
        obniz.ad1.start()
        assert_send(obniz, [{"ad1": {"stream": True}}])

        receive_json(obniz, [{"ad1": 1}])
        assert obniz.ad1.value == 1

        obniz.ad1.end()
        assert_send(obniz, [{"ad1": None}])

        assert_finished(obniz)
