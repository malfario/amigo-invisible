import pytest
from datetime import datetime
from amigo_invisible import Participante, sorteo, Sorteo
import amigo_invisible


def test_empty_bag():
    participantes = [
        Participante(nombre='luis', email='luis@example.com', excludes={'carlos'}),
        Participante(nombre='carlos', email='carlos@example.com', excludes={'luis'}),
        Participante(nombre='adela', email='adela@example.com'),
    ]
    with pytest.raises(sorteo.EmptyBag):
        sorteo.new(maestro='luis', participantes=participantes)


def test_sorteo():
    participantes = [
        Participante(nombre='luis', email='luis@example.com'),
        Participante(nombre='carlos', email='carlos@example.com'),
    ]
    s = sorteo.new(maestro='luis', participantes=participantes)
    assert s.is_valid()

    resultado = s.parejas
    assert len(resultado) == 2
    assert resultado[0][0] == resultado[1][1]
    assert resultado[0][1] == resultado[1][0]


def test_to_json():
    participantes = [
        Participante(nombre='luis', email='luis@example.com'),
        Participante(nombre='carlos', email='carlos@example.com'),
    ]
    s = sorteo.new(maestro='luis', participantes=participantes)
    doc = s.to_json()
    assert doc['maestro'] == 'luis'
    assert type(datetime.fromisoformat(doc['fecha'])) == datetime


def test_from_json():
    participantes = [
        Participante(nombre='luis', email='luis@example.com'),
        Participante(nombre='carlos', email='carlos@example.com'),
    ]
    s = sorteo.new(maestro='luis', participantes=participantes)
    doc = s.to_json()
    ss = Sorteo.from_json(doc)
    assert ss == s
