from typing import List, Tuple, Iterator, Set
from dataclasses import dataclass, field
import logging
import random
from .participante import Participante


class EmptyBag(Exception):
    """La bolsa está vacía y algún participante no está emparejado"""


def pair_generator(
    participantes: List[Participante],
) -> Iterator[Tuple[Participante, Participante]]:

    log = logging.getLogger(__name__)
    seleccionados: Set[str] = set()
    nombres = set([x.nombre for x in participantes])

    for participante in participantes:
        log.debug(f'participante: {participante}')

        excludes = participante.excludes | seleccionados
        excludes.add(participante.nombre)
        log.debug(f'excludes: {excludes}')

        rest = list(nombres - excludes)
        log.debug(f'rest: {rest}')
        if not rest:
            raise EmptyBag('La bolsa está vacía')

        elegido = random.choice(rest)
        log.debug(f'elegido: {elegido}')

        seleccionados.add(elegido)
        log.debug('----')

        yield (
            participante,
            next(x for x in participantes if x.nombre == elegido),
        )


def sorteo(
    participantes: List[Participante],
) -> List[Tuple[Participante, Participante]]:
    log = logging.getLogger(__name__)
    sorteo = []
    random.shuffle(participantes)
    for participante, elegido in pair_generator(participantes):
        log.debug(f'{participante} regala a {elegido}')
        log.debug('----')
        sorteo.append((participante, elegido))
    return sorteo
