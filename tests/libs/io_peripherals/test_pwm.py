import pytest

from ...utils import assert_finished, assert_send


class TestPeripheralPWM:
    def test_getpwm(self, obniz):
        pwm = obniz.get_free_pwm()

        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_getpwm_double(self, obniz):
        pwm1 = obniz.get_free_pwm()
        pwm2 = obniz.get_free_pwm()

        assert_finished(obniz)
        assert pwm1 == obniz.pwm0
        assert pwm2 == obniz.pwm1

    def test_getpwm_released(self, obniz):
        pwm1 = obniz.get_free_pwm()
        assert pwm1 == obniz.pwm0
        pwm1.start({"io": 11})
        assert_send(obniz, [{"io11": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io11": {"pull_type": "float"}}])
        assert_send(obniz, [{"pwm0": {"io": 11}}])

        pwm1.end()
        assert_send(obniz, [{"pwm0": None}])

        pwm2 = obniz.get_free_pwm()
        assert pwm2 == obniz.pwm0
        assert_finished(obniz)

    def test_start_io(self, obniz):
        pwm = obniz.get_free_pwm()
        pwm.start({"io": 11})

        assert_send(obniz, [{"io11": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io11": {"pull_type": "float"}}])
        assert_send(obniz, [{"pwm0": {"io": 11}}])
        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_start_io_with_drive_pull(self, obniz):
        pwm = obniz.get_free_pwm()
        pwm.start({"io": 11, "drive": "open-drain", "pull": "5v"})

        assert_send(obniz, [{"io11": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io11": {"pull_type": "pull-up5v"}}])
        assert_send(obniz, [{"pwm0": {"io": 11}}])
        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_start_io_invalid(self, obniz):
        pwm = obniz.get_free_pwm()

        with pytest.raises(Exception, match="io 15 is not valid io"):
            pwm.start({"io": 15})

        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_freq(self, obniz):
        pwm = obniz.get_free_pwm()
        pwm.start({"io": 10})
        assert_send(obniz, [{"io10": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io10": {"pull_type": "float"}}])
        assert_send(obniz, [{"pwm0": {"io": 10}}])
        pwm.freq(1000)
        assert_send(obniz, [{"pwm0": {"freq": 1000}}])

        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_pulse(self, obniz):
        pwm = obniz.get_free_pwm()
        pwm.start({"io": 9})
        assert_send(obniz, [{"io9": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io9": {"pull_type": "float"}}])
        assert_send(obniz, [{"pwm0": {"io": 9}}])
        pwm.freq(500)
        assert_send(obniz, [{"pwm0": {"freq": 500}}])
        pwm.pulse(0.5)
        assert_send(obniz, [{"pwm0": {"pulse": 0.5}}])

        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_duty(self, obniz):
        pwm = obniz.get_free_pwm()
        pwm.start({"io": 9})
        assert_send(obniz, [{"io9": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io9": {"pull_type": "float"}}])
        assert_send(obniz, [{"pwm0": {"io": 9}}])
        pwm.freq(500)
        assert_send(obniz, [{"pwm0": {"freq": 500}}])
        pwm.duty(0.5)
        assert_send(obniz, [{"pwm0": {"pulse": 0.01}}])

        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_modulate(self, obniz):
        pwm = obniz.get_free_pwm()
        pwm.start({"io": 11})  # start pwm. output at io11
        assert_send(obniz, [{"io11": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io11": {"pull_type": "float"}}])
        assert_send(obniz, [{"pwm0": {"io": 11}}])
        pwm.freq(38000)  # set pwm frequency to 38khz
        assert_send(obniz, [{"pwm0": {"freq": 38000}}])

        # signal for room heater's remote signal
        arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        pwm.modulate("am", 0.07, arr)  # am modulate. symbol length = 70usec.

        assert_send(
            obniz,
            [
                {
                    "pwm0": {
                        "modulate": {"data": arr, "symbol_length": 0.07, "type": "am"}
                    }
                }
            ],
        )
        assert_finished(obniz)
        assert pwm == obniz.pwm0

    def test_end(self, obniz):
        pwm = obniz.get_free_pwm()
        pwm.start({"io": 11})
        assert_send(obniz, [{"io11": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io11": {"pull_type": "float"}}])
        assert_send(obniz, [{"pwm0": {"io": 11}}])
        pwm.end()
        assert_send(obniz, [{"pwm0": None}])
        assert_finished(obniz)
        assert pwm == obniz.pwm0
