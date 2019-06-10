from time import sleep

from ...utils import assert_finished, assert_obniz, assert_send, receive_json


class TestObnizSwitch:
    def test_onchange(self, mocker, obniz):
        stub = mocker.stub()
        obniz.switch.onchange = stub
        assert_obniz(obniz)
        assert stub.call_count == 0

        receive_json(obniz, [{"switch": {"state": "none"}}])

        assert stub.call_count == 1
        assert stub.call_args[0][0] == "none"

        assert_finished(obniz)

    # it.skip('not value changd  , but it detect "action":get on onchange func(self, obniz):
    #     stub = sinon.stub()
    #     obniz.switch.onchange = stub
    #     assert_obniz(obniz)
    #     assert stub.call_count == 0)

    #     receive_json(obniz, [
    #     { "switch": { "state": 'push', "action": 'get' } },
    #     ])

    #     assert stub.call_count == 0)

    #     assert_finished(obniz)
    # })

    def test_input_wait_left(self, obniz):
        def callback(result):
            assert result == "left"

        obniz.switch.get_wait().add_done_callback(callback)

        assert_obniz(obniz)
        assert_send(obniz, [{"switch": "get"}])
        assert_finished(obniz)

        sleep(0.01)
        receive_json(obniz, [{"switch": {"state": "left", "action": "get"}}])

    def test_state_wait(self, obniz):
        before = True

        def callback(result):
            assert before is False

        obniz.switch.state_wait("push").add_done_callback(callback)

        assert_obniz(obniz)
        receive_json(obniz, [{"switch": {"state": "left"}}])
        assert_finished(obniz)

        receive_json(obniz, [{"switch": {"state": "right"}}])
        assert_finished(obniz)

        sleep(0.01)
        before = False
        receive_json(obniz, [{"switch": {"state": "push"}}])
