import json
from amigo_invisible import participante, Participante


def test_from_json():
    s = '''
    {
        "participantes": [
            {"nombre": "rafa", "email": "rafa@example.com", "excludes": ["adela"]},
            {"nombre": "adela", "email": "adela@example.com", "excludes": ["rafa"]},
            {"nombre": "luis", "email": "luis@example.com"}
        ]
    }
    '''

    parsed = json.loads(s)
    participantes = [Participante.from_json(x) for x in parsed['participantes']]
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


def test_to_json():
    p = Participante(nombre='rafa', email='rafa@example.com', excludes={'pepe'})
    doc = p.to_json()
    assert doc['nombre'] == 'rafa'
    assert doc['email'] == 'rafa@example.com'
    assert doc['excludes'] == ['pepe']
