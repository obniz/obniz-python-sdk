import asyncio

import pytest

from .utils import release_obnize, setup_obniz, receive_json, assert_send


@pytest.fixture(autouse=True)
def _event_loop():
    # Python 3.14: asyncio.get_event_loop() no longer creates a loop
    # implicitly, so register a fresh one for each test.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    try:
        # let cleanup tasks run first — websockets' server.close() releases
        # its listen socket in a task, so cancelling it would leak the port
        loop.run_until_complete(asyncio.sleep(0.02))
        # then cancel whatever is still running (ws connect/recv loops etc.)
        # so closing the loop does not leak "Event loop is closed" errors
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        if pending:
            loop.run_until_complete(
                asyncio.gather(*pending, return_exceptions=True)
            )
    finally:
        loop.close()
        asyncio.set_event_loop(None)


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

