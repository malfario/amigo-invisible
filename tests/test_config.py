from amigo_invisible import Participante
import amigo_invisible


def test_config_parser(config):
    prefs = amigo_invisible.Config.parse_json(config)
    assert prefs.foo == 'test'
    assert prefs.participantes == [
        Participante(
            nombre='rafael', email='rafael@example.com', excludes=['patricia']
        ),
        Participante(
            nombre='patricia', email='patricia@example.com', excludes=['rafael']
        ),
        Participante(nombre='alberto', email='alberto@example.com', excludes=['ada']),
        Participante(nombre='ada', email='ada@example.com', excludes=['alberto']),
        Participante(
            nombre='cristina', email='cristina@example.com', excludes=['carlos']
        ),
        Participante(
            nombre='carlos',
            email='carlos@example.com',
            excludes=['cristina', 'adela', 'luis'],
        ),
        Participante(
            nombre='luis', email='luis@example.com', excludes=['adela', 'carlos']
        ),
        Participante(
            nombre='adela', email='adela@example.com', excludes=['luis', 'carlos']
        ),
        Participante(nombre='jose', email='jose@example.com', excludes=[]),
        Participante(nombre='elisa', email='elisa@example.com', excludes=[]),
        Participante(nombre='marta', email='marta@example.com', excludes=[]),
    ]