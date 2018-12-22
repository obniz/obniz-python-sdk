import pytest

from .utils import release_obnize, setup_obniz


@pytest.fixture(scope="function")
def obniz(mocker):
    obniz = setup_obniz(mocker)
    yield obniz
    release_obnize(obniz)
