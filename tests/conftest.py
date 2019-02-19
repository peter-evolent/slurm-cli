import pytest


@pytest.fixture
def jsonfile(tmpdir):
    f = tmpdir.join('config.json')
    return f
