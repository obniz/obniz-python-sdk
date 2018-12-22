import pytest

from ....utils import assert_finished, assert_send, receive_json


class TestBLEAfterConnnected:
    @pytest.fixture
    def peripheral(self, mocker, obniz):
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

        return peripheral

    def test_callback_default_function_onconnect(self, peripheral):
        # assert peripheral.onconnect).to.have.not.throws()
        peripheral.onconnect()

    def test_callback_default_function_ondisconnect(self, peripheral):
        # assert peripheral.ondisconnect).to.have.not.throws()
        peripheral.ondisconnect()

    def test_callback_default_function_ondiscoverservice(self, peripheral):
        # assert peripheral.ondiscoverservice).to.have.not.throws()
        peripheral.ondiscoverservice()

    def test_callback_default_function_ondiscoverservicefinish(self, peripheral):
        # assert peripheral.ondiscoverservicefinished).to.have.not.throws()
        peripheral.ondiscoverservicefinished()

    def test_callback_default_function_onerror(self, peripheral):
        # assert peripheral.onerror).to.have.not.throws()
        peripheral.onerror()

    def test_rssi(self, peripheral):
        assert peripheral.rssi < 0

    def test_to_string(self, peripheral):
        s = str(peripheral)
        assert (
            s
            == '{"address":"e5f678800700","addressType":"public","advertisement":[2,1,26],'
            + '"rssi":-82,"scanResponse":[]}'
        )

    def test_disconnect(self, obniz, peripheral):
        peripheral.disconnect()
        assert_send(obniz, [{"ble": {"disconnect": {"address": "e5f678800700"}}}])
        assert_finished

    def test_discover_service(self, obniz, peripheral):
        peripheral = peripheral
        peripheral.discover_all_services()
        assert_send(obniz, [{"ble": {"get_services": {"address": "e5f678800700"}}}])
        assert_finished

    def test_discover_service_results(self, mocker, obniz, peripheral):
        peripheral = peripheral
        peripheral.ondiscoverservice = mocker.stub()
        peripheral.discover_all_services()
        assert_send(obniz, [{"ble": {"get_services": {"address": "e5f678800700"}}}])
        assert_finished

        assert peripheral.ondiscoverservice.call_count == 0
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_service_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",
                        }
                    }
                }
            ],
        )

        assert peripheral.ondiscoverservice.call_count == 1
        assert len(peripheral.ondiscoverservice.call_args[0]) == 1

        service = peripheral.ondiscoverservice.call_args[0][0]
        assert isinstance(service, object)
        assert service.get_peripheral() == peripheral
        assert service.uuid == "ff00"
        assert service == peripheral.get_service("FF00")

    def test_discover_service_results_finished(self, mocker, obniz, peripheral):
        peripheral = peripheral
        peripheral.ondiscoverservicefinished = mocker.stub()
        peripheral.discover_all_services()
        assert_send(obniz, [{"ble": {"get_services": {"address": "e5f678800700"}}}])
        assert_finished

        assert peripheral.ondiscoverservicefinished.call_count == 0
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_service_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",
                        }
                    }
                }
            ],
        )

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_service_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF01",
                        }
                    }
                }
            ],
        )

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_service_result": {
                            "address": "e5f678800701",
                            "service_uuid": "FF01",
                        }
                    }
                }
            ],
        )

        assert peripheral.ondiscoverservicefinished.call_count == 0

        receive_json(
            obniz, [{"ble": {"get_service_result_finish": {"address": "e5f678800700"}}}]
        )

        assert peripheral.ondiscoverservicefinished.call_count == 1
        assert len(peripheral.ondiscoverservicefinished.call_args[0]) == 1

        services = peripheral.ondiscoverservicefinished.call_args[0][0]
        assert len(services) == 2
        assert isinstance(services[0], object)
        assert services[0].get_peripheral() == peripheral
        assert services[0].uuid == "ff00"
        assert services[0] == peripheral.get_service("FF00")
        assert isinstance(services[1], object)
        assert services[1].get_peripheral() == peripheral
        assert services[1].uuid == "ff01"
        assert services[1] == peripheral.get_service("FF01")

    def test_discover_service_results2(self, mocker, obniz, peripheral):
        peripheral = peripheral
        peripheral.ondiscoverservice = mocker.stub()
        peripheral.discover_all_services()
        assert_send(obniz, [{"ble": {"get_services": {"address": "e5f678800700"}}}])
        assert_finished

        assert peripheral.ondiscoverservice.call_count == 0
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_service_result": {
                            "address": "e5f678800701",
                            "service_uuid": "FF00",
                        }
                    }
                }
            ],
        )

        assert peripheral.ondiscoverservice.call_count == 0

    def test_discover_characteristic(self, obniz, peripheral):
        peripheral = peripheral
        peripheral.get_service("FF00").discover_all_characteristics()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "get_characteristics": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_discover_characteristics_results(self, mocker, obniz, peripheral):
        peripheral = peripheral
        service = peripheral.get_service("FF00")
        service.ondiscovercharacteristic = mocker.stub()
        service.discover_all_characteristics()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "get_characteristics": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                        }
                    }
                }
            ],
        )
        assert_finished

        assert service.ondiscovercharacteristic.call_count == 0
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_characteristic_result": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "properties": ["read", "write"],
                        }
                    }
                }
            ],
        )

        assert service.ondiscovercharacteristic.call_count == 1
        assert len(service.ondiscovercharacteristic.call_args[0]) == 1

        chara = service.ondiscovercharacteristic.call_args[0][0]
        assert isinstance(chara, object)
        assert chara.get_service() == service
        assert chara.uuid == "ff01"
        assert chara == service.get_characteristic("FF01")
        assert chara.can_write() is True
        assert chara.can_read() is True
        assert chara.can_notify() is False
        assert chara.can_indicate() is False

    def test_discover_characteristics_results2(self, mocker, obniz, peripheral):
        peripheral = peripheral
        service = peripheral.get_service("FF00")
        service.ondiscovercharacteristic = mocker.stub()
        service.discover_all_characteristics()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "get_characteristics": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                        }
                    }
                }
            ],
        )
        assert_finished

        assert service.ondiscovercharacteristic.call_count == 0
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_characteristic_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF01",
                            "characteristic_uuid": "FF01",
                            "properties": ["read", "write"],
                        }
                    }
                }
            ],
        )

        assert service.ondiscovercharacteristic.call_count == 0

    def test_discover_descriptor(self, obniz, peripheral):
        peripheral = peripheral
        peripheral.get_service("FF00").get_characteristic(
            "FF01"
        ).discover_all_descriptors()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "get_descriptors": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_discover_descriptor_results(self, mocker, obniz, peripheral):
        peripheral = peripheral
        chara = peripheral.get_service("FF00").get_characteristic("FF01")
        chara.ondiscoverdescriptor = mocker.stub()
        chara.discover_all_descriptors()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "get_descriptors": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                        }
                    }
                }
            ],
        )
        assert_finished

        assert chara.ondiscoverdescriptor.call_count == 0
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_descriptor_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",
                            "characteristic_uuid": "FF01",
                            "descriptor_uuid": "2901",
                        }
                    }
                }
            ],
        )

        assert chara.ondiscoverdescriptor.call_count == 1
        assert len(chara.ondiscoverdescriptor.call_args[0]) == 1

        desc = chara.ondiscoverdescriptor.call_args[0][0]
        assert isinstance(desc, object)
        assert desc.get_characteristic() == chara
        assert desc.uuid == "2901"
        assert desc == chara.get_descriptor("2901")

    def test_discover_descriptor_results2(self, mocker, obniz, peripheral):
        peripheral = peripheral
        chara = peripheral.get_service("FF00").get_characteristic("FF01")
        chara.ondiscoverdescriptor = mocker.stub()
        chara.discover_all_descriptors()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "get_descriptors": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                        }
                    }
                }
            ],
        )
        assert_finished

        assert chara.ondiscoverdescriptor.call_count == 0
        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "get_descriptor_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",
                            "characteristic_uuid": "FF02",
                            "descriptor_uuid": "2901",
                        }
                    }
                }
            ],
        )

        assert chara.ondiscoverdescriptor.call_count == 0

    def test_write(self, obniz, peripheral):
        peripheral = peripheral
        peripheral.get_service("FF00").get_characteristic("FF01").write([0x01, 0xE8])
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "write_characteristic": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "data": [0x01, 0xE8],
                            "needResponse": True,
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_onwrite(self, mocker, obniz, peripheral):
        peripheral = peripheral

        stub = mocker.stub()
        chara = peripheral.get_service("FF00").get_characteristic("FF01")
        chara.write([0x01, 0xE8])
        chara.onwrite = stub
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "write_characteristic": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "data": [0x01, 0xE8],
                            "needResponse": True,
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "write_characteristic_result": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",  # hex string
                            "characteristic_uuid": "FF01",  # hex string
                            "result": "success",  # success or failed
                        }
                    }
                }
            ],
        )
        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1

        assert stub.call_args[0][0] == "success"
        assert_finished

    def test_onwrite_failed(self, mocker, obniz, peripheral):
        peripheral = peripheral

        stub = mocker.stub()
        chara = peripheral.get_service("FF00").get_characteristic("FF01")
        chara.onwrite = stub
        chara.write([0x01, 0xE8])
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "write_characteristic": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "data": [0x01, 0xE8],
                            "needResponse": True,
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "write_characteristic_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",  # hex string
                            "characteristic_uuid": "FF01",  # hex string
                            "result": "failed",  # success or failed
                        }
                    }
                }
            ],
        )
        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1

        assert stub.call_args[0][0] == "failed"
        assert_finished

    def test_read(self, mocker, obniz, peripheral):
        peripheral = peripheral

        stub = mocker.stub()
        chara = peripheral.get_service("FF00").get_characteristic("FF01")
        chara.onread = stub
        chara.read()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "read_characteristic": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "read_characteristic_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",  # hex string
                            "characteristic_uuid": "FF01",  # hex string
                            "result": "success",
                            "data": [0x2E, 0x22, 0x97],  # success or failed
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1

        assert stub.call_args[0][0] == [0x2E, 0x22, 0x97]

        assert_finished

    def test_write_descriptor(self, obniz, peripheral):
        peripheral = peripheral
        peripheral.get_service("FF00").get_characteristic("FF01").get_descriptor(
            "2901"
        ).write([0x01, 0xE8])
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "write_descriptor": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "descriptor_uuid": "2901",
                            "needResponse": True,
                            "data": [0x01, 0xE8],
                        }
                    }
                }
            ],
        )
        assert_finished

    def test_onwrite_descriptor(self, mocker, obniz, peripheral):
        peripheral = peripheral

        stub = mocker.stub()
        descriptor = (
            peripheral.get_service("FF00")
            .get_characteristic("FF01")
            .get_descriptor("2901")
        )
        descriptor.write([0x01, 0xE8])
        descriptor.onwrite = stub
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "write_descriptor": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "descriptor_uuid": "2901",
                            "data": [0x01, 0xE8],
                            "needResponse": True,
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "write_descriptor_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",  # hex string
                            "characteristic_uuid": "FF01",  # hex string
                            "descriptor_uuid": "2901",
                            "result": "success",  # success or failed
                        }
                    }
                }
            ],
        )
        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1

        assert stub.call_args[0][0] == "success"
        assert_finished

    def test_onwrite_descriptor_failed(self, mocker, obniz, peripheral):
        peripheral = peripheral

        stub = mocker.stub()
        descriptor = (
            peripheral.get_service("FF00")
            .get_characteristic("FF01")
            .get_descriptor("2901")
        )
        descriptor.onwrite = stub
        descriptor.write([0x01, 0xE8])
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "write_descriptor": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "descriptor_uuid": "2901",
                            "data": [0x01, 0xE8],
                            "needResponse": True,
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "write_descriptor_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",  # hex string
                            "characteristic_uuid": "FF01",  # hex string
                            "descriptor_uuid": "2901",
                            "result": "failed",  # success or failed
                        }
                    }
                }
            ],
        )
        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1

        assert stub.call_args[0][0] == "failed"
        assert_finished

    def test_read_descriptor(self, mocker, obniz, peripheral):
        peripheral = peripheral

        stub = mocker.stub()
        descriptor = (
            peripheral.get_service("FF00")
            .get_characteristic("FF01")
            .get_descriptor("2901")
        )
        descriptor.onread = stub
        descriptor.read()
        assert_send(
            obniz,
            [
                {
                    "ble": {
                        "read_descriptor": {
                            "address": "e5f678800700",
                            "service_uuid": "ff00",
                            "characteristic_uuid": "ff01",
                            "descriptor_uuid": "2901",
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "read_descriptor_result": {
                            "address": "e5f678800700",
                            "service_uuid": "FF00",  # hex string
                            "characteristic_uuid": "FF01",  # hex string
                            "descriptor_uuid": "2901",
                            "data": [0x2E, 0x22, 0x97],  # success or failed
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1

        assert stub.call_args[0][0] == [0x2E, 0x22, 0x97]

        assert_finished

    def test_error(self, mocker, obniz, peripheral):
        stub = mocker.stub()
        peripheral = peripheral
        peripheral.get_service("ff00").get_characteristic("ff01").get_descriptor(
            "ff01"
        ).onerror = stub
        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "error": {
                            "error_code": 1,
                            "module_error_code": 1,
                            "function_code": 1,
                            "message": "ERROR MESSAGE",
                            "address": "e5f678800700",  # hex string or null
                            "service_uuid": "ff00",  # hex string or null
                            "characteristic_uuid": "FF01",  # hex string or null
                            "descriptor_uuid": "FF01",  # hex string or null
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1
        assert stub.call_args[0][0]["message"] == "ERROR MESSAGE"

        assert_finished

    def test_error2(self, mocker, obniz, peripheral):
        stub = mocker.stub()
        peripheral = peripheral
        peripheral.get_service("ff00").onerror = stub
        assert stub.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "ble": {
                        "error": {
                            "error_code": 1,
                            "message": "ERROR MESSAGE",
                            "address": "e5f678800700",  # hex string or null
                            "service_uuid": "FF00",  # hex string or null
                        }
                    }
                }
            ],
        )

        assert stub.call_count == 1
        assert len(stub.call_args[0]) == 1
        assert stub.call_args[0][0]["message"] == "ERROR MESSAGE"

        assert_finished
