import pytest
from amigo_invisible import Participante, EmptyBag
import amigo_invisible


def test_empty_bag():
    participantes = [
        Participante(nombre='luis', email='luis@example.com', excludes={'carlos'}),
        Participante(nombre='carlos', email='carlos@example.com', excludes={'luis'}),
        Participante(nombre='adela', email='adela@example.com'),
    ]
    with pytest.raises(EmptyBag):
        amigo_invisible.sorteo(participantes)


def test_sorteo():
    participantes = [
        Participante(nombre='luis', email='luis@example.com'),
        Participante(nombre='carlos', email='carlos@example.com'),
    ]
    resultado = amigo_invisible.sorteo(participantes)
    assert len(resultado) == 2
    assert resultado[0][0] == resultado[1][1]
    assert resultado[0][1] == resultado[1][0]