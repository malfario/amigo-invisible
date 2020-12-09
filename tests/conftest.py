import pytest
from amigo_invisible import Participante


@pytest.fixture
def config():
    return {
        'foo': 'test',
        'participantes': {
            'rafael': ('rafael@example.com', ['patricia']),
            'patricia': ('patricia@example.com', ['rafael']),
            'alberto': ('alberto@example.com', ['ada']),
            'ada': ('ada@example.com', ['alberto']),
            'cristina': ('cristina@example.com', ['carlos']),
            'carlos': ('carlos@example.com', ['cristina', 'adela', 'luis']),
            'luis': ('luis@example.com', ['adela', 'carlos']),
            'adela': ('adela@example.com', ['luis', 'carlos']),
            'jose': ('jose@example.com', []),
            'elisa': ('elisa@example.com', []),
            'marta': ('marta@example.com', []),
        },
    }
