import json
from amigo_invisible import participante, Participante


def test_from_json():
    jsonstr = '''
    {
        "participantes": [
            {"nombre": "rafa", "email": "rafa@example.com", "excludes": ["adela"]},
            {"nombre": "adela", "email": "adela@example.com", "excludes": ["rafa"]},
            {"nombre": "luis", "email": "luis@example.com"}
        ]
    }
    '''

    parsed = json.loads(jsonstr)
    participantes = participante.from_json(parsed['participantes'])
    assert len(participantes) == 3
    assert participantes[0] == Participante(
        nombre='rafa', email='rafa@example.com', excludes={'adela'}
    )
    assert participantes[1] == Participante(
        nombre='adela', email='adela@example.com', excludes={'rafa'}
    )
    assert participantes[2] == Participante(
        nombre='luis', email='luis@example.com', excludes=set()
    )