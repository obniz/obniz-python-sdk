import pytest

from tests.utils import assert_send, assert_finished

class TestLED:
    def test_wired(self, obniz):
        obniz.wired('LED', { "anode": 0, "cathode": 1 })
        assert_send(obniz, [{ "io0": False }])
        assert_send(obniz, [{ "io1": False }])
        assert_send(obniz, [{
            "display": {
                "pin_assign": {
                    "0": {
                        "module_name": "LED",
                        "pin_name": "anode"
                    },
                    "1": {
                        "module_name": "LED",
                        "pin_name": "cathode"
                    }
                }
            }
        }])
        assert_finished(obniz)
    
    def test_wired_error_with_no_keys(self, obniz):
        with pytest.raises(Exception):
            obniz.wired('LED', {})
        assert_finished(obniz)

    def test_wired_error_with_no_arg(self, obniz):
        with pytest.raises(Exception):
            obniz.wired('LED')
        assert_finished(obniz)

    def test_wired_only_anode(self, obniz):
        obniz.wired('LED', { "anode": 10 })
        assert_send(obniz, [{ "io10": False }])
        assert_send(obniz, [{
            "display": {
                "pin_assign": {
                    "10": {
                        "module_name": "LED",
                        "pin_name": "anode"
                    }
                }
            }
        }])
        assert_finished(obniz)

    def test_on_off(self, obniz):
        led = obniz.wired('LED', { "anode": 0, "cathode": 1 })
        assert_send(obniz, [{ "io0": False }])
        assert_send(obniz, [{ "io1": False }])
        assert_send(obniz, [{
            "display": {
                "pin_assign": {
                    "0": {
                        "module_name": "LED",
                        "pin_name": "anode"
                    },
                    "1": {
                        "module_name": "LED",
                        "pin_name": "cathode"
                    }
                }
            }
        }])
        assert_finished(obniz)
        
        led.on()
        assert_send(obniz, [{
            "io": {
                "animation": {
                    "name": led.animation_name,
                    "status": "pause"
                }
            }
        }])
        assert_send(obniz, [{ "io0": True }])
        assert_finished(obniz)

        led.off()
        assert_send(obniz, [{
            "io": {
                "animation": {
                    "name": led.animation_name,
                    "status": "pause"
                }
            }
        }])
        assert_send(obniz, [{ "io0": False }])
        assert_finished(obniz)
