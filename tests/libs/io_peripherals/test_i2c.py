from time import sleep

from ...utils import assert_finished, assert_send, receive_json


class TestPeripheralI2C:
    def test_start(self, obniz):
        obniz.i2c0.start(
            {"mode": "master", "sda": 2, "scl": 3, "clock": 400000, "pull": None}
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io3": {"pull_type": "float"}}])
        assert_send(
            obniz, [{"i2c0": {"clock": 400000, "sda": 2, "scl": 3, "mode": "master"}}]
        )
        assert_finished(obniz)

    def test_start_with_gnd(self, obniz):
        obniz.i2c0.start(
            {
                "mode": "master",
                "sda": 2,
                "scl": 3,
                "clock": 400000,
                "pull": None,
                "gnd": 0,
            }
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io3": {"pull_type": "float"}}])
        assert_send(obniz, [{"io0": False}])
        # assert_send(obniz, [
        # {
        #     display: {
        #     pin_assign: {
        #         '0': {
        #         module_name: 'i2c0',
        #         pin_name: 'gnd',
        #         },
        #     },
        #     },
        # },
        # ])
        assert_send(
            obniz, [{"i2c0": {"clock": 400000, "sda": 2, "scl": 3, "mode": "master"}}]
        )
        assert_finished(obniz)

    def test_end(self, obniz):
        obniz.i2c0.start(
            {"mode": "master", "sda": 2, "scl": 3, "clock": 400000, "pull": "5v"}
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "pull-up5v"}}])
        assert_send(obniz, [{"io3": {"pull_type": "pull-up5v"}}])
        assert_send(
            obniz, [{"i2c0": {"clock": 400000, "sda": 2, "scl": 3, "mode": "master"}}]
        )

        obniz.i2c0.end()
        assert_send(obniz, [{"i2c0": None}])

    def test_write(self, obniz):
        obniz.i2c0.start(
            {"mode": "master", "sda": 2, "scl": 3, "clock": 400000, "pull": "5v"}
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "pull-up5v"}}])
        assert_send(obniz, [{"io3": {"pull_type": "pull-up5v"}}])
        assert_send(
            obniz, [{"i2c0": {"clock": 400000, "sda": 2, "scl": 3, "mode": "master"}}]
        )

        obniz.i2c0.write(0x50, [0x00, 0x00, 0x12])
        assert_send(obniz, [{"i2c0": {"address": 0x50, "data": [0x00, 0x00, 0x12]}}])

    # it.skip('write10bit', function() {
    #     obniz.i2c0.start({
    #     "mode": 'master',
    #     "sda": 2,
    #     "scl": 3,
    #     "clock": 100000,
    #     "pull": '3v',
    #     })
    #     assert_send(obniz, [{ "io2": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io3": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io2": { "pull_type": 'pull-up5v' } }])
    #     assert_send(obniz, [{ "io3": { "pull_type": 'pull-up5v' } }])
    #     assert_send(obniz, [
    #     { "i2c0": { "clock": 100000, "sda": 2, "scl": 3, "mode": 'master' } },
    #     ])

    #     obniz.i2c0.write10bit(0x50, [0x00, 0x00, 0x12])
    #     assert_send(obniz, [
    #     {
    #         "i2c0": {
    #         "address": 0x50,
    #         address_type: '10bit',
    #         "data": [0x00, 0x00, 0x12],
    #         },
    #     },
    #     ])
    # })

    def test_read_wait(self, obniz):
        obniz.i2c0.start(
            {"mode": "master", "sda": 2, "scl": 3, "clock": 100000, "pull": "3v"}
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "pull-up3v"}}])
        assert_send(obniz, [{"io3": {"pull_type": "pull-up3v"}}])
        assert_send(
            obniz, [{"i2c0": {"clock": 100000, "sda": 2, "scl": 3, "mode": "master"}}]
        )

        def callback(value):
            assert value == [0x61, 0xF2, 0x1F]
            assert_finished(obniz)

        obniz.i2c0.read_wait(0x50, 3)

        assert_send(obniz, [{"i2c0": {"address": 0x50, "read": 3}}])

        sleep(0.01)
        receive_json(
            obniz,
            [{"i2c0": {"mode": "master", "address": 0x50, "data": [0x61, 0xF2, 0x1F]}}],
        )

    # it.skip('readWait invalid length', function() {
    #     obniz.i2c0.start({
    #     "mode": 'master',
    #     "sda": 2,
    #     "scl": 3,
    #     "clock": 100000,
    #     "pull": '3v',
    #     })
    #     assert_send(obniz, [{ "io2": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io3": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io2": { "pull_type": 'pull-up3v' } }])
    #     assert_send(obniz, [{ "io3": { "pull_type": 'pull-up3v' } }])
    #     assert_send(obniz, [
    #     { "i2c0": { "clock": 100000, "sda": 2, "scl": 3, "mode": 'master' } },
    #     ])

    #     r = obniz.i2c0.readWait(0x50, 3).then(
    #     function(value) {
    #         assert value).to.lengthOf(3)
    #         assert_finished(obniz)
    #     }.bind(self)
    #     )

    #     assert_send(obniz, [{ "i2c0": { "address": 0x50, "read": 3 } }])
    #     setTimeout(
    #     function() {
    #         receive_json(obniz, [
    #         { "i2c0": { "address": 0x50, "data": [0x61, 0xf2] } },
    #         ])
    #     }.bind(self),
    #     10
    #     )
    #     return r
    # })
    # it.skip('readWait withothers', function() {
    #     obniz.i2c0.start({
    #     "mode": 'master',
    #     "sda": 2,
    #     "scl": 3,
    #     "clock": 100000,
    #     pullType: 'pull-up3v',
    #     })
    #     assert_send(obniz, [{ "io2": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io3": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io2": { "pull_type": 'pull-up3v' } }])
    #     assert_send(obniz, [{ "io3": { "pull_type": 'pull-up3v' } }])
    #     assert_send(obniz, [
    #     { "i2c0": { "clock": 100000, "sda": 2, "scl": 3, "mode": 'master' } },
    #     ])

    #     r = obniz.i2c0.readWait(0x50, 3).then(
    #     function(value) {
    #         assert value).to.be.deep.equal([0x61, 0xf2, 0x1f])
    #         assert_finished(obniz)
    #     }.bind(self)
    #     )

    #     assert_send(obniz, [{ "i2c0": { "address": 0x50, "read": 3 } }])
    #     setTimeout(
    #     function() {
    #         receive_json(obniz, [
    #         { "i2c0": { "address": 0x51, "data": [0xaa, 0xbb, 0xcc] } },
    #         ])
    #         receive_json(obniz, [
    #         { "i2c0": { "address": 0x50, "data": [0x61, 0xf2, 0x1f] } },
    #         ])
    #     }.bind(self),
    #     10
    #     )
    #     return r
    # })

    # it.skip('readWait10bit', function() {
    #     obniz.i2c0.start({
    #     "mode": 'master',
    #     "sda": 2,
    #     "scl": 3,
    #     "clock": 100000,
    #     "pull": '3v',
    #     })
    #     assert_send(obniz, [{ "io2": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io3": { "output_type": 'open-drain' } }])
    #     assert_send(obniz, [{ "io2": { "pull_type": 'pull-up3v' } }])
    #     assert_send(obniz, [{ "io3": { "pull_type": 'pull-up3v' } }])
    #     assert_send(obniz, [
    #     { "i2c0": { "clock": 100000, "sda": 2, "scl": 3, "mode": 'master' } },
    #     ])

    #     r = obniz.i2c0.read10bitWait(0x50, 3).then(
    #     function(value) {
    #         assert value).to.be.deep.equal([0x61, 0xf2, 0x1f])
    #         assert_finished(obniz)
    #     }.bind(self)
    #     )

    #     assert_send(obniz, [
    #     { "i2c0": { "address": 0x50, address_type: '10bit', "read": 3 } },
    #     ])
    #     setTimeout(
    #     function() {
    #         receive_json(obniz, [
    #         { "i2c0": { "address": 0x50, "data": [0x61, 0xf2, 0x1f] } },
    #         ])
    #     }.bind(self),
    #     10
    #     )
    #     return r
    # })

    def test_slave_start(self, obniz):
        obniz.i2c0.start(
            {"mode": "slave", "sda": 2, "scl": 3, "slave_address": 1, "pull": None}
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io3": {"pull_type": "float"}}])
        assert_send(
            obniz, [{"i2c0": {"slave_address": 1, "sda": 2, "scl": 3, "mode": "slave"}}]
        )
        assert_finished(obniz)

    def test_slave_data_get(self, mocker, obniz):
        obniz.i2c0.start(
            {"mode": "slave", "sda": 2, "scl": 3, "slave_address": 1, "pull": None}
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io3": {"pull_type": "float"}}])
        assert_send(
            obniz, [{"i2c0": {"slave_address": 1, "sda": 2, "scl": 3, "mode": "slave"}}]
        )
        assert_finished(obniz)

        obniz.i2c0.onwritten = mocker.stub()
        assert obniz.i2c0.onwritten.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "i2c0": {
                        "mode": "slave",
                        "address": 1,
                        "is_fragmented": True,
                        "data": [16, 34, 242],
                    }
                }
            ],
        )

        assert obniz.i2c0.onwritten.call_count == 1
        assert len(obniz.i2c0.onwritten.call_args[0]) == 2

        assert obniz.i2c0.onwritten.call_args[0][0] == [16, 34, 242]

        assert obniz.i2c0.onwritten.call_args[0][1] == 1

    def test_slave_data_another_data(self, mocker, obniz):
        obniz.i2c0.start(
            {"mode": "slave", "sda": 2, "scl": 3, "slave_address": 1, "pull": None}
        )
        assert_send(obniz, [{"io2": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io3": {"output_type": "open-drain"}}])
        assert_send(obniz, [{"io2": {"pull_type": "float"}}])
        assert_send(obniz, [{"io3": {"pull_type": "float"}}])
        assert_send(
            obniz, [{"i2c0": {"slave_address": 1, "sda": 2, "scl": 3, "mode": "slave"}}]
        )
        assert_finished(obniz)

        obniz.i2c0.onwritten = mocker.stub()
        assert obniz.i2c0.onwritten.call_count == 0

        receive_json(
            obniz,
            [
                {
                    "i2c0": {
                        "mode": "slave",
                        "address": 2,
                        "is_fragmented": True,
                        "data": [16, 34, 242],
                    }
                }
            ],
        )

        assert obniz.i2c0.onwritten.call_count == 1
        assert len(obniz.i2c0.onwritten.call_args[0]) == 2

        assert obniz.i2c0.onwritten.call_args[0][0] == [16, 34, 242]

        assert obniz.i2c0.onwritten.call_args[0][1] == 2
