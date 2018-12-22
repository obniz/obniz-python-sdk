import pytest

from ....utils import assert_finished, assert_send, receive_json


class TestBle:
    @pytest.fixture(autouse=True)
    def before_each(self, obniz):
        service = obniz.ble.service({"uuid": "FFF0"})
        characteristic = obniz.ble.characteristic({"uuid": "FFF1", "text": "Hi"})
        descriptor = obniz.ble.descriptor(
            {"uuid": "2901", "text": "hello wrold characteristic"}
        )

        service.add_characteristic(characteristic)
        characteristic.add_descriptor(descriptor)

        obniz.ble.peripheral.add_service(service)

        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "services": [
                                {
                                    "characteristics": [
                                        {
                                            "data": [72, 105],
                                            "descriptors": [
                                                {
                                                    "data": [
                                                        104,
                                                        101,
                                                        108,
                                                        108,
                                                        111,
                                                        32,
                                                        119,
                                                        114,
                                                        111,
                                                        108,
                                                        100,
                                                        32,
                                                        99,
                                                        104,
                                                        97,
                                                        114,
                                                        97,
                                                        99,
                                                        116,
                                                        101,
                                                        114,
                                                        105,
                                                        115,
                                                        116,
                                                        105,
                                                        99,
                                                    ],
                                                    "uuid": "2901",
                                                }
                                            ],
                                            "uuid": "fff1",
                                        }
                                    ],
                                    "uuid": "fff0",
                                }
                            ]
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_onconnection_updates(self, mocker, obniz):
        obniz.ble.peripheral.onconnectionupdates = mocker.stub()

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "connection_status": {
                                "address": "77e754ab8591",
                                "status": "connected",
                            }
                        }
                    }
                }
            ],
        )
        assert obniz.ble.peripheral.onconnectionupdates.call_count == 1
        assert len(obniz.ble.peripheral.onconnectionupdates.call_args[0]) == 1
        assert obniz.ble.peripheral.onconnectionupdates.call_args[0][0] == {
            "address": "77e754ab8591",
            "status": "connected",
        }
        assert_finished

    def test_disconnected(self, mocker, obniz):
        obniz.ble.peripheral.onconnectionupdates = mocker.stub()

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "connection_status": {
                                "address": "77e754ab8591",
                                "status": "disconnected",
                            }
                        }
                    }
                }
            ],
        )
        assert obniz.ble.peripheral.onconnectionupdates.call_count == 1
        assert len(obniz.ble.peripheral.onconnectionupdates.call_args[0]) == 1
        assert obniz.ble.peripheral.onconnectionupdates.call_args[0][0] == {
            "address": "77e754ab8591",
            "status": "disconnected",
        }
        assert_finished

    def test_end(self, obniz):
        obniz.ble.peripheral.end()

        assert_send(obniz, [{"ble": {"peripheral": None}}])
        assert_finished

    def test_unknown_service(self, obniz):
        service = obniz.ble.peripheral.get_service("FFFF")
        assert service is None

    def test_unknown_characteristic(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("00F1")
        assert chara is None

    def test_unknown_descriptor(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("0000")
        assert desciptor is None

    def test_callback_default_function_chara_onread(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        # assert chara.onread).to.have.not.throws()
        chara.onread(None)

    def test_callback_default_function_chara_onwrite(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        # assert chara.onwrite).to.have.not.throws()
        chara.onwrite()

    def test_callback_default_function_chara_onwritefromremote(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        # assert chara.onwritefromremote).to.have.not.throws()
        chara.onwritefromremote()

    def test_callback_default_function_chara_onreadfromremote(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        # assert chara.onreadfromremote).to.have.not.throws()
        chara.onreadfromremote()

    def test_callback_default_function_descriptor_onread(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        descriptor = chara.get_descriptor("2901")
        # assert descriptor.onread).to.have.not.throws()
        descriptor.onread(None)

    def test_callback_default_function_descriptor_onwrite(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        descriptor = chara.get_descriptor("2901")
        # assert descriptor.onwrite).to.have.not.throws()
        descriptor.onwrite()

    def test_callback_default_function_descriptor_onwritefromremote(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        descriptor = chara.get_descriptor("2901")
        # assert descriptor.onwritefromremote).to.have.not.throws()
        descriptor.onwritefromremote()

    def test_callback_default_function_descriptor_onreadfromremote(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        descriptor = chara.get_descriptor("2901")
        # assert descriptor.onreadfromremote).to.have.not.throws()
        descriptor.onreadfromremote()

    def test_write_char(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        chara.write([0x23, 0x83, 0x6E, 0xFC])
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "write_characteristic": {
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "data": [0x23, 0x83, 0x6E, 0xFC],
                            }
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_write_char2(self, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        chara.write_number(0x23)
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "write_characteristic": {
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "data": [0x23],
                            }
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_write_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        chara.onwrite = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "write_characteristic_result": {
                                "service_uuid": "FFF0",
                                "characteristic_uuid": "FFF1",
                                "result": "success",
                            }
                        }
                    }
                }
            ],
        )

        assert len(chara.onwrite.call_args[0]) == 1
        assert chara.onwrite.call_args[0][0] == "success"
        assert_finished

    def test_notify_write_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        chara.onwritefromremote = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "notify_write_characteristic": {
                                "address": "77e754ab8591",
                                "service_uuid": "FFF0",
                                "characteristic_uuid": "FFF1",
                                "data": [16, 34, 242],
                            }
                        }
                    }
                }
            ],
        )

        assert len(chara.onwritefromremote.call_args[0]) == 2
        assert chara.onwritefromremote.call_args[0][0] == "77e754ab8591"
        assert chara.onwritefromremote.call_args[0][1] == [16, 34, 242]
        assert_finished

    def test_read_char(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        chara.read()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_characteristic": {
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                            }
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_read_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        chara.onread = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_characteristic_result": {
                                "service_uuid": "FFF0",
                                "characteristic_uuid": "FFF1",
                                "data": [16, 34, 242],
                                "result": "success",
                            }
                        }
                    }
                }
            ],
        )

        assert len(chara.onread.call_args[0]) == 1
        assert chara.onread.call_args[0][0] == [16, 34, 242]
        assert_finished

    def test_notify_read_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        chara.onreadfromremote = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "notify_read_characteristic": {
                                "address": "77e754ab8591",
                                "service_uuid": "FFF0",
                                "characteristic_uuid": "FFF1",
                            }
                        }
                    }
                }
            ],
        )

        assert len(chara.onreadfromremote.call_args[0]) == 1
        assert chara.onreadfromremote.call_args[0][0] == "77e754ab8591"
        assert_finished

    def test_write_descriptor(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("2901")
        desciptor.write([16, 34, 242])
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "write_descriptor": {
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "descriptor_uuid": "2901",
                                "data": [16, 34, 242],
                            }
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_write_descriptor2(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("2901")
        desciptor.write_number(16)
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "write_descriptor": {
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "descriptor_uuid": "2901",
                                "data": [16],
                            }
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_write_descriptor_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("2901")
        desciptor.onwrite = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "write_descriptor_result": {
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "descriptor_uuid": "2901",
                                "result": "success",
                            }
                        }
                    }
                }
            ],
        )

        assert len(desciptor.onwrite.call_args[0]) == 1
        assert desciptor.onwrite.call_args[0][0] == "success"
        assert_finished

    def test_notify_descriptor_write_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("2901")
        desciptor.onwritefromremote = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "notify_write_descriptor": {
                                "address": "77e754ab8591",
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "descriptor_uuid": "2901",
                                "data": [16, 34, 242],
                            }
                        }
                    }
                }
            ],
        )

        assert len(desciptor.onwritefromremote.call_args[0]) == 2
        assert desciptor.onwritefromremote.call_args[0][0] == "77e754ab8591"
        assert desciptor.onwritefromremote.call_args[0][1] == [16, 34, 242]
        assert_finished

    def test_read_descriptor(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("2901")
        desciptor.read()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_descriptor": {
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "descriptor_uuid": "2901",
                            }
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_read_descriptor_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("2901")
        desciptor.onread = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_descriptor_result": {
                                "service_uuid": "FFF0",
                                "characteristic_uuid": "FFF1",
                                "descriptor_uuid": "2901",
                                "data": [16, 34, 242],
                                "result": "success",
                            }
                        }
                    }
                }
            ],
        )

        assert len(desciptor.onread.call_args[0]) == 1
        assert desciptor.onread.call_args[0][0] == [16, 34, 242]
        assert_finished

    def test_notify_descriptor_read_results(self, mocker, obniz):
        service = obniz.ble.peripheral.get_service("FFF0")
        chara = service.get_characteristic("FFF1")
        desciptor = chara.get_descriptor("2901")
        desciptor.onreadfromremote = mocker.stub()
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "notify_read_descriptor": {
                                "address": "77e754ab8591",
                                "service_uuid": "fff0",
                                "characteristic_uuid": "fff1",
                                "descriptor_uuid": "2901",
                            }
                        }
                    }
                }
            ],
        )

        assert len(desciptor.onreadfromremote.call_args[0]) == 1
        assert desciptor.onreadfromremote.call_args[0][0] == "77e754ab8591"
        assert_finished
