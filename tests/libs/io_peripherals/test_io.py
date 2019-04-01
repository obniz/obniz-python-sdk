from time import sleep

import pytest

from ...utils import assert_finished, assert_obniz, assert_send, receive_json


class TestPeripheralIO:
    @pytest.mark.parametrize("input,expected", [(True, True), (1, True), (0, False)])
    def test_output(self, obniz, input, expected):
        obniz.io0.output(input)
        assert_obniz(obniz)
        assert_send(obniz, [{"io0": expected}])
        assert_finished(obniz)

    def test_output_over_pin(self, obniz):
        with pytest.raises(
            AttributeError, match=r"'Obniz' object has no attribute 'io20'"
        ):

            obniz.io20.output(True)

        assert_finished(obniz)

    @pytest.mark.parametrize(
        "input,expected",
        [("5v", "push-pull5v"), ("3v", "push-pull3v"), ("open-drain", "open-drain")],
    )
    def test_drive(self, obniz, input, expected):
        obniz.io1.drive(input)
        assert_obniz(obniz)
        assert_send(obniz, [{"io1": {"output_type": expected}}])
        assert_finished(obniz)

    @pytest.mark.parametrize(
        "input,error_message",
        [
            (None, "please specify drive methods in string"),
            ("3.3v", "unknown drive method"),
        ],
    )
    def test_drive_error(self, obniz, input, error_message):
        with pytest.raises(Exception, match=error_message):
            obniz.io1.drive(input)

        assert_finished(obniz)

    @pytest.mark.parametrize(
        "input,expected",
        [
            ("5v", "pull-up5v"),
            ("3v", "pull-up3v"),
            ("0v", "pull-down"),
            (None, "float"),
        ],
    )
    def test_pull(self, obniz, input, expected):
        obniz.io3.pull(input)
        assert_obniz(obniz)
        assert_send(obniz, [{"io3": {"pull_type": expected}}])
        assert_finished(obniz)

    def test_input(self, mocker, obniz):
        stub = mocker.stub()
        obniz.io7.input(stub)
        assert_obniz(obniz)
        assert_send(obniz, [{"io7": {"direction": "input", "stream": True}}])

        receive_json(obniz, [{"io7": True}])
        assert stub.call_count == 1
        assert stub.call_args[0][0] is True

        receive_json(obniz, [{"io7": False}])
        assert stub.call_count == 2
        assert stub.call_args[0][0] is False

        assert_finished(obniz)

    def test_input_wait_true(self, obniz):
        # def callback(result):
        #     assert result is True

        obniz.io8.input_wait()

        assert_obniz(obniz)
        assert_send(obniz, [{"io8": {"direction": "input", "stream": False}}])
        assert_finished(obniz)
        sleep(0.01)
        receive_json(obniz, [{"io8": True}])

    def test_end(self, obniz):
        obniz.io0.end()
        assert_obniz(obniz)
        assert_send(obniz, [{"io0": None}])
        assert_finished(obniz)

    # TODO: 怪しい
    def test_input_wait_false(self, obniz):
        # def callback(result):
        #     pass

        obniz.io9.input_wait()
        assert_obniz(obniz)
        assert_send(obniz, [{"io9": {"direction": "input", "stream": False}}])
        assert_finished(obniz)
        sleep(0.01)
        receive_json(obniz, [{"io10": True}])

    def test_io_animation(self, obniz):
        def state1(index):
            # index = 0
            obniz.io0.output(False)
            obniz.io1.output(True)

        def state2(index):
            # index = 1
            obniz.io0.output(True)
            obniz.io1.output(False)

        obniz.io.animation(
            "animation-1",
            "loop",
            [{"duration": 10, "state": state1}, {"duration": 10, "state": state2}],
        )
        assert_obniz(obniz)
        assert_send(
            obniz,
            [
                {
                    "io": {
                        "animation": {
                            "name": "animation-1",
                            "status": "loop",
                            "states": [
                                {
                                    "duration": 10,
                                    "state": [{"io0": False}, {"io1": True}],
                                },
                                {
                                    "duration": 10,
                                    "state": [{"io0": True}, {"io1": False}],
                                },
                            ],
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_io_animation_pause(self, obniz):
        obniz.io.animation("animation-1", "pause")
        assert_send(
            obniz, [{"io": {"animation": {"name": "animation-1", "status": "pause"}}}]
        )

    def test_io_animation_pause2(self, obniz):
        obniz.io.animation("anim", "pause")
        assert_send(obniz, [{"io": {"animation": {"name": "anim", "status": "pause"}}}])

    def test_io_animation_resume(self, obniz):
        obniz.io.animation("a", "resume")
        assert_send(obniz, [{"io": {"animation": {"name": "a", "status": "resume"}}}])
        assert_finished(obniz)

    def test_input_simple(self, obniz):
        obniz.send({"io1": "get"})
        assert_send(obniz, [{"io1": "get"}])
        assert_finished(obniz)

    def test_output_detail(self, obniz):
        obniz.send({"io0": {"direction": "output", "value": True}})
        assert_send(obniz, [{"io0": {"direction": "output", "value": True}}])
        assert_finished(obniz)
