from ....utils import assert_finished, assert_send, receive_json


class TestBleCentral:
    def test_scan(self, obniz):
        obniz.ble.scan.start(None, {"duration": 10})

        assert_send(obniz, [{"ble": {"scan": {"duration": 10}}}])
        assert_finished

    def test_scan_default(self, obniz):
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])
        assert_finished

    def test_scan_stop(self, obniz):
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])
        obniz.ble.scan.end()
        assert_send(obniz, [{"ble": {"scan": None}}])
        assert_finished

    def test_callback_default_function_onfind(self, obniz):
        # assert obniz.ble.scan.onfind).to.have.not.throws()
        obniz.ble.scan.onfind()

    def test_callback_default_function_onfindfinish(self, obniz):
        # assert obniz.ble.scan.onfinish).to.have.not.throws()
        obniz.ble.scan.onfinish()

    def test_on_scan(self, mocker, obniz):
        stub = mocker.stub()

        obniz.ble.scan.onfind = stub
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])

        results = [
            {
                "ble": {
                    "scan_result": {
                        "address": "e5f678800700",
                        "device_type": "dumo",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -82,
                        "adv_data": [
                            2,
                            1,
                            26,
                            26,
                            255,
                            76,
                            0,
                            2,
                            21,
                            201,
                            97,
                            172,
                            167,
                            148,
                            166,
                            64,
                            120,
                            177,
                            255,
                            150,
                            44,
                            178,
                            85,
                            204,
                            219,
                            61,
                            131,
                            104,
                            10,
                            200,
                        ],
                        "flag": 26,
                        "scan_resp": [
                            22,
                            9,
                            83,
                            83,
                            83,
                            83,
                            83,
                            83,
                            83,
                            101,
                            114,
                            118,
                            105,
                            99,
                            101,
                            55,
                            56,
                            58,
                            70,
                            54,
                            58,
                            69,
                            53,
                        ],
                    }
                }
            }
        ]

        receive_json(obniz, results)

        assert stub.call_count == 1
        peripheral = stub.call_args[0][0]
        assert isinstance(peripheral, object)

        assert peripheral.adv_data == [
            2,
            1,
            26,
            26,
            255,
            76,
            0,
            2,
            21,
            201,
            97,
            172,
            167,
            148,
            166,
            64,
            120,
            177,
            255,
            150,
            44,
            178,
            85,
            204,
            219,
            61,
            131,
            104,
            10,
            200,
        ]
        assert peripheral.scan_resp == [
            22,
            9,
            83,
            83,
            83,
            83,
            83,
            83,
            83,
            101,
            114,
            118,
            105,
            99,
            101,
            55,
            56,
            58,
            70,
            54,
            58,
            69,
            53,
        ]
        assert peripheral.local_name == "SSSSSSService78:F6:E5"
        assert peripheral.ibeacon == {
            "major": 15747,
            "minor": 26634,
            "power": 200,
            "rssi": -82,
            "uuid": "c961aca7-94a6-4078-b1ff-962cb255ccdb",
        }

        assert_finished

    def test_on_scan2(self, mocker, obniz):
        stub = mocker.stub()

        obniz.ble.scan.onfind = stub
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])

        results = [
            {
                "ble": {
                    "scan_result": {
                        "address": "e5f678800700",
                        "device_type": "dumo",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -82,
                        "adv_data": [2, 1, 26],
                        "flag": 26,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results)

        assert stub.call_count == 1
        peripheral = stub.call_args[0][0]
        assert isinstance(peripheral, object)

        assert peripheral.adv_data == [2, 1, 26]
        assert peripheral.local_name is None
        assert peripheral.ibeacon is None

        assert_finished

    def test_on_scan_with_target(self, mocker, obniz):
        stub = mocker.stub()

        obniz.ble.scan.onfind = stub
        target = {
            "uuids": ["FFF0"],  # scan only has uuids "FFF0" and "FFF1"
            "local_name": "obniz-BLE",  # scan only has local_name "obniz-BLE"
        }

        setting = {"duration": 10}

        obniz.ble.scan.start(target, setting)

        assert_send(obniz, [{"ble": {"scan": {"duration": 10}}}])
        results = [
            {
                "ble": {
                    "scan_result": {
                        "address": "05e41890858c",
                        "device_type": "ble",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -48,
                        "adv_data": [2, 1, 6, 7, 255, 76, 0, 16, 2, 11, 0],
                        "flag": 6,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results)
        assert stub.call_count == 0

        results2 = [
            {
                "ble": {
                    "scan_result": {
                        "address": "e5f678800700",
                        "device_type": "ble",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -48,
                        "adv_data": [
                            2,
                            1,
                            6,
                            10,
                            9,
                            111,
                            98,
                            110,
                            105,
                            122,
                            45,
                            66,
                            76,
                            69,
                            3,
                            2,
                            0xF0,
                            0xFF,
                        ],
                        "flag": 6,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results2)
        assert stub.call_count == 1

        peripheral = stub.call_args[0][0]
        assert isinstance(peripheral, object)

        assert peripheral.adv_data == [
            2,  # flag
            1,
            6,
            10,  # local_name
            9,
            111,
            98,
            110,
            105,
            122,
            45,
            66,
            76,
            69,
            3,  # uuid
            2,
            0xF0,
            0xFF,
        ]
        assert peripheral.local_name == "obniz-BLE"
        assert peripheral.ibeacon is None

        assert_finished

    def test_on_scan_with_target2(self, mocker, obniz):
        stub = mocker.stub()

        obniz.ble.scan.onfind = stub
        target = {
            "uuids": [
                "713d0000-503e-4c75-ba94-3148f18d9400"
            ]  # scan only has uuids "FFF0" and "FFF1"
        }

        setting = {"duration": 10}

        obniz.ble.scan.start(target, setting)

        assert_send(obniz, [{"ble": {"scan": {"duration": 10}}}])
        results = [
            {
                "ble": {
                    "scan_result": {
                        "address": "05e41890858c",
                        "device_type": "ble",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -48,
                        "adv_data": [2, 1, 6, 7, 255, 76, 0, 16, 2, 11, 0],
                        "flag": 6,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results)
        assert stub.call_count == 0

        results3 = [
            {
                "ble": {
                    "scan_result": {
                        "address": "05e41890858d",
                        "device_type": "ble",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -48,
                        "adv_data": [
                            0x02,
                            0x01,
                            0x06,
                            0x11,
                            0x06,
                            0x00,
                            0x94,
                            0x8D,
                            0xF1,
                            0x48,
                            0x31,
                            0x94,
                            0xBA,
                            0x75,
                            0x4C,
                            0x3E,
                            0x50,
                            0x00,
                            0x00,
                            0x3D,
                            0x72,
                        ],
                        "flag": 6,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results3)
        assert stub.call_count == 0

        results2 = [
            {
                "ble": {
                    "scan_result": {
                        "address": "e5f678800700",
                        "device_type": "ble",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -48,
                        "adv_data": [
                            0x02,
                            0x01,
                            0x06,
                            0x11,
                            0x06,
                            0x00,
                            0x94,
                            0x8D,
                            0xF1,
                            0x48,
                            0x31,
                            0x94,
                            0xBA,
                            0x75,
                            0x4C,
                            0x3E,
                            0x50,
                            0x00,
                            0x00,
                            0x3D,
                            0x71,
                        ],
                        "flag": 6,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results2)
        assert stub.call_count == 1

        peripheral = stub.call_args[0][0]
        assert isinstance(peripheral, object)

        assert peripheral.adv_data == [
            0x02,
            0x01,
            0x06,
            0x11,
            0x06,
            0x00,
            0x94,
            0x8D,
            0xF1,
            0x48,
            0x31,
            0x94,
            0xBA,
            0x75,
            0x4C,
            0x3E,
            0x50,
            0x00,
            0x00,
            0x3D,
            0x71,
        ]
        assert peripheral.local_name is None
        assert peripheral.ibeacon is None

        assert_finished

    def test_on_scan_finished(self, mocker, obniz):
        stub1 = mocker.stub()
        stub2 = mocker.stub()

        obniz.ble.scan.onfind = stub1
        obniz.ble.scan.onfinish = stub2
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])

        results = [{"ble": {"scan_result_finish": True}}]

        receive_json(obniz, results)

        assert stub1.call_count == 0
        assert stub2.call_count == 1

        peripherals = stub2.call_args[0][0]
        assert type(peripherals) is list
        assert len(peripherals) == 0

        assert_finished

    def test_on_scan_finished2(self, mocker, obniz):
        stub1 = mocker.stub()
        stub2 = mocker.stub()

        obniz.ble.scan.onfind = stub1
        obniz.ble.scan.onfinish = stub2
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])

        results1 = [
            {
                "ble": {
                    "scan_result": {
                        "address": "e5f678800700",
                        "device_type": "dumo",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -82,
                        "adv_data": [2, 1, 26],
                        "flag": 26,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results1)

        assert stub1.call_count == 1
        assert stub2.call_count == 0

        results2 = [{"ble": {"scan_result_finish": True}}]

        receive_json(obniz, results2)

        assert stub1.call_count == 1
        assert stub2.call_count == 1

        peripherals = stub2.call_args[0][0]
        assert type(peripherals) is list
        assert len(peripherals) == 1
        peripheral = peripherals[0]
        assert isinstance(peripheral, object)

        assert peripheral.adv_data == [2, 1, 26]
        assert peripheral.local_name is None
        assert peripheral.ibeacon is None

        assert_finished

    def test_connect(self, mocker, obniz):
        stub = mocker.stub()

        obniz.ble.scan.onfind = stub
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])

        results = [
            {
                "ble": {
                    "scan_result": {
                        "address": "e5f678800700",
                        "device_type": "dumo",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -82,
                        "adv_data": [2, 1, 26],
                        "flag": 26,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results)

        assert stub.call_count == 1
        peripheral = stub.call_args[0][0]
        assert isinstance(peripheral, object)

        connect_stub = mocker.stub()
        peripheral.onconnect = connect_stub
        peripheral.connect()

        assert_send(obniz, [{"ble": {"connect": {"address": "e5f678800700"}}}])

        assert connect_stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "status_update": {
                            "address": "e5f678800700",
                            "status": "connected",
                        }
                    }
                }
            ],
        )

        assert connect_stub.call_count == 1

        assert_finished

    def test_disconnect(self, mocker, obniz):
        stub = mocker.stub()

        obniz.ble.scan.onfind = stub
        obniz.ble.scan.start()

        assert_send(obniz, [{"ble": {"scan": {"duration": 30}}}])

        results = [
            {
                "ble": {
                    "scan_result": {
                        "address": "e5f678800700",
                        "device_type": "dumo",
                        "address_type": "public",
                        "ble_event_type": "connectable_advertisemnt",
                        "rssi": -82,
                        "adv_data": [2, 1, 26],
                        "flag": 26,
                        "scan_resp": [],
                    }
                }
            }
        ]

        receive_json(obniz, results)

        assert stub.call_count == 1
        peripheral = stub.call_args[0][0]
        assert isinstance(peripheral, object)

        connect_stub = mocker.stub()
        disconnect_stub = mocker.stub()
        peripheral.onconnect = connect_stub
        peripheral.ondisconnect = disconnect_stub
        peripheral.connect()

        assert_send(obniz, [{"ble": {"connect": {"address": "e5f678800700"}}}])

        assert connect_stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "status_update": {
                            "address": "e5f678800700",
                            "status": "disconnected",
                        }
                    }
                }
            ],
        )

        assert connect_stub.call_count == 0
        assert disconnect_stub.call_count == 1

        assert_finished
