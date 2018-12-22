from ...utils import assert_finished, assert_send, receive_json


class TestObnizMeasure:
    def test_echo(self, obniz):
        obniz.measure.echo(
            {
                "io_pulse": 1,  # io for generate pulse
                "io_echo": 2,  # io to be measured
                "pulse": "positive",  # generate pulse pattern
                "pulse_width": 0.1,  # generate pulse width
                "measure_edges": 3,  # 1 to 4. maximum edges to measure
                "timeout": 1000,  # self is optional. 1000(1sec) is default
            }
        )

        assert_send(
            obniz,
            [
                {
                    "measure": {
                        "echo": {
                            "io_pulse": 1,
                            "io_echo": 2,
                            "pulse": "positive",
                            "pulse_width": 0.1,
                            "measure_edges": 3,
                            "timeout": 1000,
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_echo_response(self, mocker, obniz):
        stub = mocker.stub()
        obniz.measure.echo(
            {
                "io_pulse": 1,  # io for generate pulse
                "io_echo": 2,  # io to be measured
                "pulse": "positive",  # generate pulse pattern
                "pulse_width": 0.1,  # generate pulse width
                "measure_edges": 3,  # 1 to 4. maximum edges to measure
                "timeout": 1000,  # self is optional. 1000(1sec) is default
                "callback": stub,
            }
        )

        assert_send(
            obniz,
            [
                {
                    "measure": {
                        "echo": {
                            "io_pulse": 1,
                            "io_echo": 2,
                            "pulse": "positive",
                            "pulse_width": 0.1,
                            "measure_edges": 3,
                            "timeout": 1000,
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)

        receive_json(obniz, [{"measure": {"echo": [{"edge": True, "timing": 500}]}}])

        assert len(stub.call_args[0]) == 1
        assert stub.call_args[0][0] == [{"edge": True, "timing": 500}]
