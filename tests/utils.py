import asyncio
import json

import asynctest
import pytest
import websockets

from obniz import Obniz
from .obniz_json_validator import obniz_json_validator as validator

server_data_count = 0
error_data_count = 0


def create_server(port, on_connection):
    wss = websockets.serve(on_connection, "localhost", port)

    return asyncio.get_event_loop().run_until_complete(wss)


def create_obniz(port, obniz_id):
    return Obniz(obniz_id, {"obniz_server": "ws://localhost:" + str(port)})


def setup_obniz(mocker):
    global server_data_count

    stub = mocker.MagicMock(buffered_amount=0)
    # stub.on = mocker.stub()
    stub.send = asynctest.CoroutineMock()
    # stub.close = mocker.stub()
    # stub.removeAllListeners = mocker.stub()

    mocker.patch("obniz.Obniz.wsconnect")
    obniz = create_obniz(100, "12345678")
    obniz.socket = stub
    obniz.error = mocker.stub()
    # obniz.`ws_on_open`()
    obniz.firmware_ver = "1.0.3"

    server_data_count = 0

    return obniz


def release_obnize(obniz):
    obniz.close()
    # Obniz.prototype.wsconnect.restore()


def receive_json(obniz, json_val):
    results = validator.response_validate(json_val, "json")
    assert results["valid"], results["errors"]

    obniz.ws_on_message(json.dumps(json_val))


def assert_obniz(obniz):
    assert isinstance(obniz, Obniz)


def assert_send(obniz, expected):
    global server_data_count

    count = server_data_count
    server_data_count += 1

    stub = obniz.socket.send

    message = (
        "[obniz.send] no more send data. (called "
        + str(stub.call_count)
        + " times, but you expect "
        + str(count + 1)
        + " times) "
    )
    assert stub.call_count > count, message

    assert_json(stub.call_args_list[count][0][0], "[obniz.send]invalid json")
    val = json.loads(stub.call_args_list[count][0][0])
    assert val == expected, val + " != " + expected

    validate_errors = validator.request_validate(val, "json")
    assert validate_errors["valid"], validate_errors["errors"]


def assert_finished(obniz):
    stub = obniz.socket.send
    message = (
        "[obniz.send] not finished. (send: called "
        + str(stub.call_count)
        + " times, but you expect "
        + str(server_data_count)
        + " times) "
    )
    assert stub.call_count == server_data_count, message

    error_stub = obniz.error
    message = (
        "[obniz.send] not finished. (error: called "
        + str(error_stub.call_count)
        + " times, but you expect "
        + str(error_data_count)
        + " times) "
    )
    assert error_stub.call_count == error_data_count, message


def assert_json(string, message):
    assert type(string) is str, message
    try:
        json.loads(string)
    except Exception:
        pytest.fail(message)
