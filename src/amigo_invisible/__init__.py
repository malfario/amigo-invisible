import random
from typing import List
from datetime import datetime, timezone
from .sorteo import Sorteo, pair_generator, EmptyBag
from .participante import Participante


def sorteo(
    maestro: str,
    participantes: List[Participante],
) -> Sorteo:
    parejas = []

    random.shuffle(participantes)
    for participante, elegido in pair_generator(participantes):
        if elegido is None:
            raise EmptyBag("Bolsa vacía")
        parejas.append((participante.nombre, elegido.nombre))

    return Sorteo(
        fecha=datetime.now(timezone.utc),
        maestro=maestro,
        participantes=participantes,
        parejas=parejas,
    )
