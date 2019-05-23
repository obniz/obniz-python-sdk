from time import sleep

import pytest

from ...utils import assert_finished, assert_send, receive_json


class TestPeripheralSPI:
    def test_start(self, obniz):
        obniz.spi0.start(
            {"clk": 0, "frequency": 1000000, "miso": 2, "mode": "master", "mosi": 1}
        )

        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(
            obniz,
            [
                {
                    "spi0": {
                        "clk": 0,
                        "clock": 1000000,
                        "miso": 2,
                        "mode": "master",
                        "mosi": 1,
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_start_with_gnd(self, obniz):
        obniz.spi0.start(
            {
                "clk": 0,
                "frequency": 1000000,
                "miso": 2,
                "mode": "master",
                "mosi": 1,
                "gnd": 7,
            }
        )

        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io7": False}])
        # assert_send(obniz, [
        #     {
        #         display: {
        #         pin_assign: {
        #             '7': {
        #             module_name: 'spi0',
        #             pin_name: 'gnd',
        #             },
        #         },
        #         },
        #     },
        # ])
        assert_send(
            obniz,
            [
                {
                    "spi0": {
                        "clk": 0,
                        "clock": 1000000,
                        "miso": 2,
                        "mode": "master",
                        "mosi": 1,
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_write(self, obniz):
        obniz.spi0.start({"clk": 0, "frequency": 1000000, "miso": 2, "mode": "master"})
        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(
            obniz, [{"spi0": {"clk": 0, "clock": 1000000, "miso": 2, "mode": "master"}}]
        )

        def callback(value):
            assert value == [0x61, 0xF2]
            assert_finished(obniz)

        obniz.spi0.write_wait([0x12, 0x98])

        assert_send(obniz, [{"spi0": {"data": [0x12, 0x98], "read": True}}])
        sleep(0.01)
        receive_json(obniz, [{"spi0": {"data": [0x61, 0xF2]}}])

    def test_write_over_32_to_lt_1_0_3(self, obniz):
        firmver_ver = obniz.firmware_ver
        obniz.firmware_ver = "1.0.2"
        obniz.spi0.start({"clk": 0, "frequency": 1000000, "miso": 2, "mode": "master"})
        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(
            obniz, [{"spi0": {"clk": 0, "clock": 1000000, "miso": 2, "mode": "master"}}]
        )

        data = []
        for i in range(0, 33):
            data.append(i)

        def callback(value):
            pass

        with pytest.raises(
            Exception,
            match="with your obniz 1.0.2. spi max length=32byte but yours 33. "
            + "Please update obniz firmware",
        ):
            obniz.spi0.write_wait(data)

        assert_finished(obniz)
        obniz.firmware_ver = firmver_ver

    def test_write_over_32_to_gte_1_0_3(self, obniz):
        firmver_ver = obniz.firmware_ver
        obniz.firmware_ver = "1.0.3"
        obniz.spi0.start({"clk": 0, "frequency": 1000000, "miso": 2, "mode": "master"})
        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(
            obniz, [{"spi0": {"clk": 0, "clock": 1000000, "miso": 2, "mode": "master"}}]
        )

        data = []
        for i in range(0, 33):
            data.append(i)

        def callback(value):
            assert value == data
            assert_finished(obniz)

        obniz.spi0.write_wait(data)

        assert_send(obniz, [{"spi0": {"data": data, "read": True}}])
        sleep(0.01)
        receive_json(obniz, [{"spi0": {"data": data}}])
        obniz.firmware_ver = firmver_ver

    #   it.skip('SPI send 2byte and receive 3byte', function() {
    #     obniz.spi0.start({
    #       "clk": 0,
    #       "frequency": 1000000,
    #       "miso": 2,
    #       "mode": 'master',
    #       "mosi": 1,
    #     })
    #     assert_send(obniz, [{ "io0": { "output_type": 'push-pull5v' } }])
    #     assert_send(obniz, [{ "io1": { "output_type": 'push-pull5v' } }])
    #     assert_send(obniz, [{ "io2": { "output_type": 'push-pull5v' } }])
    #     assert_send(obniz, [{ "io0": { "pull_type": 'float' } }])
    #     assert_send(obniz, [{ "io1": { "pull_type": 'float' } }])
    #     assert_send(obniz, [{ "io2": { "pull_type": 'float' } }])
    #     assert_send(obniz, [
    #       { "spi0": { "clk": 0, "clock": 1000000, "miso": 2, "mode": 'master', "mosi": 1 } },
    #     ])

    #     r = obniz.spi0.write_wait([0x12, 0x98]).then(
    #       function(value) {
    #         expect(value).to.be.deep.equal([0x61, 0xf2])
    #         assert_finished(obniz)
    #       }.bind(self)
    #     )

    #     assert_send(obniz, [{ "spi0": { "data": [0x12, 0x98], "read": True } }])
    #     setTimeout(
    #       function() {
    #         receive_json(obniz, [
    #           { "spi0": { "data": [0x61, 0xf2, 0x34] } },
    #         ])
    #       }.bind(self),
    #       10
    #     )
    #     return r
    #   })

    def test_end(self, obniz):
        obniz.spi0.start(
            {"clk": 0, "frequency": 1000000, "miso": 2, "mode": "master", "mosi": 1}
        )

        assert_send(obniz, [{"io0": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io1": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io2": {"output_type": "push-pull5v"}}])
        assert_send(obniz, [{"io0": {"pull_type": "float"}}])
        assert_send(obniz, [{"io1": {"pull_type": "float"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(
            obniz,
            [
                {
                    "spi0": {
                        "clk": 0,
                        "clock": 1000000,
                        "miso": 2,
                        "mode": "master",
                        "mosi": 1,
                    }
                }
            ],
        )
        assert_finished(obniz)

        obniz.spi0.end()
        assert_send(obniz, [{"spi0": None}])
        assert_finished(obniz)
