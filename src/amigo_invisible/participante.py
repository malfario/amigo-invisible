from dataclasses import dataclass, field
from typing import Dict, Any, List, Set


@dataclass
class Participante:
    nombre: str
    email: str
    excludes: Set[str] = field(default_factory=set)

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'Participante':
        return Participante(
            nombre=json['nombre'],
            email=json['email'],
            excludes=set(json.get('excludes', [])),
        )

    def to_json(self) -> Dict[str, Any]:
        return dict(
            nombre=self.nombre,
            email=self.email,
            excludes=[x for x in self.excludes],
        )