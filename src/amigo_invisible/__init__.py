import random
from typing import List, Optional, Iterator
from datetime import datetime, timezone
from .sorteo import Sorteo, pair_generator, EmptyBag
from .participante import Participante


def sorteo(
    maestro: str,
    participantes: List[Participante],
) -> Iterator[Optional[Sorteo]]:
    while True:
        try:
            parejas = []
            random.shuffle(participantes)

            for participante, elegido in pair_generator(participantes):
                if elegido is None:
                    raise EmptyBag("Bolsa vacía")
                parejas.append((participante.nombre, elegido.nombre))

            yield Sorteo(
                fecha=datetime.now(timezone.utc),
                maestro=maestro,
                participantes=participantes,
                parejas=parejas,
            )

        except EmptyBag:
            yield None