from typing import List, Tuple
from dataclasses import dataclass, field
import logging
import random


@dataclass
class Participante:
    nombre: str
    email: str
    excludes: List[str] = field(default_factory=list)


class EmptyBag(Exception):
    """La bolsa está vacía y algún participante no está emparejado"""


def sorteo(
    participantes: List[Participante],
) -> List[Tuple[Participante, Participante]]:

    log = logging.getLogger(__name__)
    seleccionados: List[Tuple[str, str]] = []
    nombres = set([x.nombre for x in participantes])

    random.shuffle(participantes)
    for participante in participantes:
        log.debug(f'participante: {participante}')

        excludes = set(participante.excludes + [x for x, y in seleccionados])
        excludes.add(participante.nombre)
        log.debug(f'excludes: {excludes}')

        rest = list(nombres - excludes)
        log.debug(f'rest: {rest}')
        if not rest:
            raise EmptyBag('La bolsa está vacía')

        elegido = random.choice(rest)
        log.debug(f'elegido: {elegido}')

        seleccionados.append((elegido, participante.nombre))
        log.debug('----')

    return [
        (
            [x for x in participantes if x.nombre == m][0],
            [x for x in participantes if x.nombre == n][0],
        )
        for n, m in seleccionados
    ]
