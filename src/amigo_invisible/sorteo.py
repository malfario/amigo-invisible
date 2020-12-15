from typing import List, Tuple, Iterator, Set, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import random
import json

from .participante import Participante


class EmptyBag(Exception):
    """La bolsa está vacía y algún participante no está emparejado"""


class SorteoInvalido(Exception):
    """El sorteo no es formalmente válido"""


@dataclass
class Sorteo:
    fecha: datetime
    maestro: str
    participantes: List[Participante]
    parejas: List[Tuple[str, str]]

    def validate(self):
        def validate_pairs(parejas: List[Tuple[str, str]]) -> bool:
            participantes = set([x for x, y in parejas])
            seleccion = set([y for x, y in parejas])
            return participantes ^ seleccion == set()

        if self.maestro.strip() == "":
            raise SorteoInvalido("No se ha especificado maestro de ceremonias")

        if not validate_pairs(self.parejas):
            raise SorteoInvalido("El emparejamiento no es vålido")

    def to_json(self) -> Dict[str, Any]:
        return dict(
            fecha=str(self.fecha),
            maestro=self.maestro,
            participantes=[x.to_json() for x in self.participantes],
            parejas=[[x, y] for x, y in self.parejas],
        )

    @staticmethod
    def from_json(doc: Dict[str, Any]) -> 'Sorteo':
        return Sorteo(
            fecha=datetime.fromisoformat(doc['fecha']),
            maestro=doc['maestro'],
            participantes=[Participante.from_json(x) for x in doc['participantes']],
            parejas=[(x, y) for x, y in doc['parejas']],
        )


def pair_generator(
    participantes: List[Participante],
) -> Iterator[Tuple[Participante, Optional[Participante]]]:
    seleccionados: Set[str] = set()
    nombres = set([x.nombre for x in participantes])

    for participante in participantes:
        excludes = participante.excludes | seleccionados
        excludes.add(participante.nombre)

        rest = list(nombres - excludes)
        if not rest:
            yield (participante, None)
            continue

        elegido = random.choice(rest)
        seleccionados.add(elegido)

        yield (
            participante,
            next(x for x in participantes if x.nombre == elegido),
        )


def save_json(sorteo: Sorteo, filename: Path) -> None:
    with open(filename, 'w') as f:
        doc = sorteo.to_json()
        json.dump(doc, f)


def load_json(filename: Path) -> Sorteo:
    with open(filename, 'r') as f:
        doc = json.load(f)
        return Sorteo.from_json(doc)