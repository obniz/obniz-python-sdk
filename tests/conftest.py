import pytest

from .utils import release_obnize, setup_obniz, receive_json, assert_send


@pytest.fixture(scope="function")
def obniz(mocker):
    obniz = setup_obniz(mocker)
    receive_json(obniz, [{'ws': {'ready': True, 'obniz': {'hw': 'obnizb1', 'firmware': '2.0.2'}}}])
    assert_send(obniz, [{'ws': {'reset_obniz_on_ws_disconnection': True}}])

    yield obniz
    release_obnize(obniz)

@pytest.fixture(scope="function")
def uninitialized_obniz(mocker):
    obniz = setup_obniz(mocker)
    yield obniz
    release_obnize(obniz)

