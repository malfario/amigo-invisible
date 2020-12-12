import pytest
from amigo_invisible import Participante, config


@pytest.fixture
def config_json():
    return {
        'foo': 'test',
    }


def test_config_parser(config_json):
    prefs = config.parse_json(config_json)
    assert prefs.foo == 'test'