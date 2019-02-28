import pytest

from ...utils import assert_finished, assert_obniz, assert_send, receive_json

class TestDisplay:
    def test_clear(self, obniz):
        obniz.display.clear()
        assert_obniz(obniz)
        assert_send(obniz, [{
            "display": {
                "clear": True
            }
        }])
        assert_finished(obniz)

    @pytest.mark.parametrize('text', ["Hello World!"])
    def test_print(self, obniz, text):
        obniz.display.print(text)
        assert_obniz(obniz)
        assert_send(obniz, [{
            "display": {
                "text": text
            }
        }])
        assert_finished(obniz)
    
    @pytest.mark.parametrize('text', ["Hello World!"])
    def test_qr_without_correction(self, obniz, text):
        obniz.display.qr(text)
        assert_obniz(obniz)
        assert_send(obniz, [{
            "display": {
                "qr": {
                    "text": text,
                    "correction": "M"
                }
            }
        }])
        assert_finished(obniz)

    @pytest.mark.parametrize(
        'text,correction',
        [
            ("Hello World!", "L"),
            ("Hello World!", "M"),
            ("Hello World!", "Q"),
            ("Hello World!", "H")
        ]
    )
    def test_qr(self, obniz, text, correction):
        obniz.display.qr(text, correction)
        assert_obniz(obniz)
        assert_send(obniz, [{
            "display": {
                "qr": {
                    "text": text,
                    "correction": correction
                }
            }
        }])
        assert_finished(obniz)
    
    @pytest.mark.parametrize('data', [[1] * 1024])
    def test_raw(self, obniz, data):
        obniz.display.raw(data)
        assert_obniz(obniz)
        assert_send(obniz, [{
            "display": {
                "raw": data
            }
        }])
        assert_finished(obniz)
    
    def test_set_pin_name(self, obniz):
        obniz.display.set_pin_name(0, "io", "input")
        assert_obniz(obniz)
        assert_send(obniz, [{
            "display": {
                "pin_assign": {
                    "0": {
                        "module_name": "io",
                        "pin_name": "input"
                    }
                }
            }
        }])
        assert_finished(obniz)

    def test_set_pin_names(self, obniz):
        obniz.display.set_pin_names("io", {
            0: "input",
            1: "output"
        })
        assert_obniz(obniz)
        assert_send(obniz, [{
            "display": {
                "pin_assign": {
                    "0": {
                        "module_name": 'io',
                        "pin_name": 'input',
                    },
                    "1": {
                        "module_name": 'io',
                        "pin_name": 'output',
                    },
                },
            }
        }])
        assert_finished(obniz)