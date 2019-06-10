import json

from obniz.obniz.libs.utils.util import ObnizUtil
from ....utils import assert_finished, assert_send, receive_json


class TestBle:
    def test_start(self, obniz):
        obniz.ble.advertisement.start()

        assert_send(obniz, [{"ble": {"advertisement": {"adv_data": []}}}])
        assert_finished

    def test_stop(self, obniz):
        obniz.ble.advertisement.end()

        assert_send(obniz, [{"ble": {"advertisement": None}}])
        assert_finished

    def test_service_generate_ad(self, obniz):
        service = obniz.ble.service({"uuid": "FFF0"})
        assert service.adv_data == {
            "flags": ["general_discoverable_mode", "br_edr_not_supported"],
            "serviceUuids": ["fff0"],
        }

        assert_finished

    def test_set_adv_raw(self, obniz):
        obniz.ble.advertisement.set_adv_data_raw(
            [0x02, 0x01, 0x1A, 0x07, 0x09, 0x53, 0x61, 0x6D, 0x70, 0x6C, 0x65]
        )
        obniz.ble.advertisement.start()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "advertisement": {
                            "adv_data": [
                                0x02,
                                0x01,
                                0x1A,
                                0x07,
                                0x09,
                                0x53,
                                0x61,
                                0x6D,
                                0x70,
                                0x6C,
                                0x65,
                            ]
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_set_adv(self, obniz):
        obniz.ble.advertisement.set_adv_data(
            {
                "flags": ["general_discoverable_mode", "br_edr_not_supported"],
                "manufacturerData": {
                    "companyCode": 0x004C,
                    "data": [
                        0x02,
                        0x15,
                        0xC2,
                        0x8F,
                        0x0A,
                        0xD5,
                        0xA7,
                        0xFD,
                        0x48,
                        0xBE,
                        0x9F,
                        0xD0,
                        0xEA,
                        0xE9,
                        0xFF,
                        0xD3,
                        0xA8,
                        0xBB,
                        0x10,
                        0x00,
                        0x00,
                        0x10,
                        0xFF,
                    ],
                },
            }
        )
        obniz.ble.advertisement.start()

        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "advertisement": {
                            "adv_data": [
                                0x02,
                                0x01,
                                0x06,
                                0x1A,
                                0xFF,
                                0x4C,
                                0x00,
                                0x02,
                                0x15,
                                0xC2,
                                0x8F,
                                0x0A,
                                0xD5,
                                0xA7,
                                0xFD,
                                0x48,
                                0xBE,
                                0x9F,
                                0xD0,
                                0xEA,
                                0xE9,
                                0xFF,
                                0xD3,
                                0xA8,
                                0xBB,
                                0x10,
                                0x00,
                                0x00,
                                0x10,
                                0xFF,
                            ]
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_set_scan_resp_raw(self, obniz):
        obniz.ble.advertisement.set_scan_resp_data_raw(
            [0x07, 0x09, 0x53, 0x61, 0x6D, 0x70, 0x6C, 0x65]
        )
        obniz.ble.advertisement.start()

        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "advertisement": {
                            "adv_data": [],
                            "scan_resp": [
                                0x07,
                                0x09,
                                0x53,
                                0x61,
                                0x6D,
                                0x70,
                                0x6C,
                                0x65,
                            ],
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_set_scan_resp(self, obniz):
        obniz.ble.advertisement.set_scan_resp_data({"localName": "obniz BLE"})
        obniz.ble.advertisement.start()

        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "advertisement": {
                            "adv_data": [],
                            "scan_resp": [
                                0x0A,
                                0x09,
                                0x6F,
                                0x62,
                                0x6E,
                                0x69,
                                0x7A,
                                0x20,
                                0x42,
                                0x4C,
                                0x45,
                            ],
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_start_service(self, obniz):
        setting = {
            "uuid": "FFF0",
            "characteristics": [
                {
                    "uuid": "FFF1",
                    "data": [0x0E, 0x00],  # data for dataArray or  text for string
                    "descriptors": [
                        {
                            "uuid": "2901",  # Characteristic User Description
                            # data for dataArray or text for string
                            "text": "hello world characteristic",
                        }
                    ],
                }
            ],
        }
        obniz.ble.peripheral.add_service(setting)

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
                                            "data": [14, 0],
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
                                                        111,
                                                        114,
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

    def test_start_service_from_object(self, obniz):
        service = obniz.ble.service({"uuid": "FFF0"})
        characteristic = obniz.ble.characteristic({"uuid": "FFF1", "text": "Hi"})
        descriptor = obniz.ble.descriptor(
            {"uuid": "2901", "text": "hello world characteristic"}
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
                                                        111,
                                                        114,
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

    def test_start_service_from_json(self, obniz):
        setting = {
            "services": [
                {
                    "uuid": "FFF0",
                    "characteristics": [
                        {
                            "uuid": "FFF1",
                            "data": [72, 105],  # data for dataArray or text for string
                            "descriptors": [
                                {
                                    "uuid": "2901",  # Characteristic User Description
                                    # data for dataArray or text for string
                                    "text": "hello world characteristic",
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        obniz.ble.peripheral.set_json(setting)

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
                                                        111,
                                                        114,
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

    def test_check_json(self, obniz):
        service = obniz.ble.service({"uuid": "FFF0"})
        characteristic = obniz.ble.characteristic({"uuid": "FFF1", "text": "Hi"})
        descriptor = obniz.ble.descriptor(
            {"uuid": "2901", "text": "hello world characteristic"}
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
                                                        111,
                                                        114,
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
                                            "data": [72, 105],
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

        service_json = ObnizUtil.json_dumps(obniz.ble.peripheral)
        assert service_json == json.dumps(
            {
                "services": [
                    {
                        "uuid": "fff0",
                        "characteristics": [
                            {
                                "uuid": "fff1",
                                "descriptors": [
                                    {
                                        "uuid": "2901",
                                        "data": [
                                            104,
                                            101,
                                            108,
                                            108,
                                            111,
                                            32,
                                            119,
                                            111,
                                            114,
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
                                    }
                                ],
                                "data": [72, 105],
                            }
                        ],
                    }
                ]
            }
        )

    def test_read_char(self, obniz):
        service = obniz.ble.service({"uuid": "1234"})
        characteristic = obniz.ble.characteristic({"uuid": "7777", "data": [1, 2, 3]})
        service.add_characteristic(characteristic)
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
                                        {"data": [1, 2, 3], "uuid": "7777"}
                                    ],
                                    "uuid": "1234",
                                }
                            ]
                        }
                    }
                }
            ],
        )
        assert_finished

        def callback(data):
            assert data == [1, 2, 3]

        characteristic.read_wait().add_done_callback(callback)

        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_characteristic": {
                                "service_uuid": "1234",
                                "characteristic_uuid": "7777",
                            }
                        }
                    }
                }
            ],
        )

        assert_finished

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_characteristic_result": {
                                "service_uuid": "1234",
                                "characteristic_uuid": "7777",
                                "data": [1, 2, 3],
                                "result": "success",
                            }
                        }
                    }
                }
            ],
        )

    def test_read_descriptor(self, obniz):
        obniz.debugpring = True
        service = obniz.ble.service({"uuid": "1234"})
        characteristic = obniz.ble.characteristic({"uuid": "7777", "data": [1, 2, 3]})
        descriptor = obniz.ble.descriptor(
            {"uuid": "2901", "text": "sample"}  # Characteristic User Description
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
                                            "data": [1, 2, 3],
                                            "descriptors": [
                                                {
                                                    "data": [
                                                        115,
                                                        97,
                                                        109,
                                                        112,
                                                        108,
                                                        101,
                                                    ],
                                                    "uuid": "2901",
                                                }
                                            ],
                                            "uuid": "7777",
                                        }
                                    ],
                                    "uuid": "1234",
                                }
                            ]
                        }
                    }
                }
            ],
        )
        assert_finished

        def callback(data):
            assert data == [115, 97, 109, 112, 108, 101]

        descriptor.read_wait().add_done_callback(callback)

        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_descriptor": {
                                "characteristic_uuid": "7777",
                                "descriptor_uuid": "2901",
                                "service_uuid": "1234",
                            }
                        }
                    }
                }
            ],
        )

        assert_finished

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "peripheral": {
                            "read_descriptor_result": {
                                "service_uuid": "1234",
                                "characteristic_uuid": "7777",
                                "descriptor_uuid": "2901",
                                "data": [115, 97, 109, 112, 108, 101],
                                "result": "success",
                            }
                        }
                    }
                }
            ],
        )
