from ...utils import assert_finished, assert_send, receive_json


class TestPeripheralUART:
    def test_start(self, obniz):
        obniz.uart0.start({"tx": 1, "rx": 2, "baud": 9600, "bits": 7})
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])

        assert_send(obniz, [{"uart0": {"tx": 1, "rx": 2, "baud": 9600, "bits": 7}}])

        obniz.uart0.send("Hi")

        assert_send(obniz, [{"uart0": {"data": [72, 105]}}])
        assert_finished(obniz)

    def test_start_with_gnd(self, obniz):
        obniz.uart0.start({"tx": 1, "rx": 2, "baud": 9600, "bits": 7, "gnd": 3})
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"io3": False}])
        # assert_send(
        #     obniz,
        #     [
        #         {
        #             "display": {
        #                 "pin_assign": {"3": {"module_name": "uart0", "pin_name": "gnd"}}
        #             }
        #         }
        #     ],
        # )

        assert_send(obniz, [{"uart0": {"tx": 1, "rx": 2, "baud": 9600, "bits": 7}}])

        obniz.uart0.send("Hi")

        assert_send(obniz, [{"uart0": {"data": [72, 105]}}])
        assert_finished(obniz)

    def test_send(self, obniz):
        obniz.uart0.start({"tx": 1, "rx": 2})  # 1 is output, 2 is input
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])

        assert_send(obniz, [{"uart0": {"tx": 1, "rx": 2}}])

        obniz.uart0.send("Hi")
        assert_send(obniz, [{"uart0": {"data": [72, 105]}}])
        obniz.uart0.send(0x11)
        assert_send(obniz, [{"uart0": {"data": [0x11]}}])
        obniz.uart0.send([0x11, 0x45, 0x44])
        assert_send(obniz, [{"uart0": {"data": [0x11, 0x45, 0x44]}}])
        assert_finished(obniz)

    def test_end(self, obniz):
        obniz.uart0.start({"tx": 1, "rx": 2})  # 1 is output, 2 is input
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"uart0": {"tx": 1, "rx": 2}}])

        obniz.uart0.send("Hi")
        assert_send(obniz, [{"uart0": {"data": [72, 105]}}])

        obniz.uart0.end()
        assert_send(obniz, [{"uart0": None}])
        assert_finished(obniz)

    def test_onreceive(self, mocker, obniz):
        obniz.uart0.start({"tx": 0, "rx": 1})  # 0 is output, 1 is input
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"uart0": {"tx": 0, "rx": 1}}])
        stub = mocker.stub()
        obniz.uart0.onreceive = stub

        receive_json(obniz, [{"uart0": {"data": [78, 105, 99, 101]}}])
        assert stub.call_count == 1
        assert stub.call_args[0][0] == [78, 105, 99, 101]
        assert stub.call_args[0][1] == "Nice"
        assert_finished(obniz)

    def test_read_bytes(self, obniz):
        obniz.uart0.start({"tx": 0, "rx": 1})  # 0 is output, 1 is input
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"uart0": {"tx": 0, "rx": 1}}])

        receive_json(obniz, [{"uart0": {"data": [78, 105, 99, 101]}}])
        receive_json(obniz, [{"uart0": {"data": [1, 2, 3]}}])

        assert obniz.uart0.is_data_exists()
        assert obniz.uart0.read_bytes() == [78, 105, 99, 101, 1, 2, 3]
        assert_finished(obniz)

    def test_read_text(self, obniz):
        obniz.uart0.start({"tx": 0, "rx": 1})  # 0 is output, 1 is input
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"uart0": {"tx": 0, "rx": 1}}])

        receive_json(obniz, [{"uart0": {"data": [78, 105, 99, 101]}}])
        receive_json(obniz, [{"uart0": {"data": [101]}}])

        assert obniz.uart0.is_data_exists()
        assert obniz.uart0.read_text() == "Nicee"
        assert_finished(obniz)
