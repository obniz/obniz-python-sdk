from ..utils import assert_finished, assert_send, receive_json


class TestSystem:
    def test_ping(self, obniz):
        unixtime = 1522840296917
        rand = 4553670


        obniz.ping_wait(unixtime, rand)
        assert_send(
            obniz,
            [
                {
                    "system": {
                        "ping": {
                            "key": [0, 0, 1, 98, 144, 90, 221, 213, 0, 69, 123, 198]
                        }
                    }
                }
            ],
        )
        assert_finished(obniz)

    def test_ping_pong(self, obniz):
        unixtime = 1522840296917
        rand = 4553670
        resolved = False

        def callback():
            nonlocal resolved
            resolved = True

        obniz.ping_wait(unixtime, rand).add_done_callback(callback)
        assert_send(
            obniz,
            [
                {
                    "system": {
                        "ping": {
                            "key": [0, 0, 1, 98, 144, 90, 221, 213, 0, 69, 123, 198]
                        }
                    }
                }
            ],
        )
        assert resolved is False
        receive_json(
            obniz,
            [
                {
                    "system": {
                        "pong": {
                            "key": [0, 0, 1, 98, 144, 90, 221, 213, 0, 69, 123, 198],
                            "obnizTime": 4553670,
                            "pingServerTime": 1522840296035,
                            "pongServerTime": 1522840297892,
                        }
                    }
                }
            ],
        )

    def test_keep_working_at_offline(self, obniz):
        obniz.keep_working_at_offline(True)
        assert_send(obniz, [{"system": {"keep_working_at_offline": True}}])
        assert_finished(obniz)

    def test_reboot(self, obniz):
        obniz.reboot()
        assert_send(obniz, [{"system": {"reboot": True}}])
        assert_finished(obniz)

    def test_reset(self, obniz):
        obniz.reset()
        assert_send(obniz, [{"system": {"reset": True}}])
        assert_finished(obniz)

    def test_self_check(self, obniz):
        obniz.self_check()
        assert_send(obniz, [{"system": {"self_check": True}}])
        assert_finished(obniz)

    def test_wait(self, obniz):
        obniz.wait(500)
        assert_send(obniz, [{"system": {"wait": 500}}])
        assert_finished(obniz)

    # TODO: Promise.raceをどうする
    # def test_wait_delay(self, obniz):
    #     function wait(ms) {
    #         return new Promise((resolve, reject) => {
    #             setTimeout(reject, ms)
    #         })
    #     }
    #     promise = Promise.race([obniz.wait(500), wait(501)])
    #     assert_send(obniz, [{"system": {"wait": 500}}])
    #     assert_finished(obniz)
    #     return promise

    # def test_wait_delay2(self, obniz):
    #     function wait(ms) {
    #         return new Promise((resolve, reject) => {
    #             setTimeout(resolve, ms)
    #         })
    #     }
    #     promise = Promise.race([
    #         obniz.wait(500).then(() => {
    #             return Promise.reject('too early')
    #         }),
    #         wait(495),
    #     ])
    #     assert_send(obniz, [{"system": {"wait": 500}}])
    #     assert_finished(obniz)
    #     return promise
