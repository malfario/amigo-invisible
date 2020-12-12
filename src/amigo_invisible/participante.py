from dataclasses import dataclass, field
from typing import Dict, Any, List, Set


@dataclass
class Participante:
    nombre: str
    email: str
    excludes: Set[str] = field(default_factory=set)


def from_json(json: List[Dict[str, Any]]) -> List[Participante]:
    return [
        Participante(
            nombre=item['nombre'],
            email=item['email'],
            excludes=set(item.get('excludes', [])),
        )
        for item in json
    ]
