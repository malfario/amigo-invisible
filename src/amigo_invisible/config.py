from typing import Dict, Any, List
from dataclasses import dataclass
from .sorteo import Participante


@dataclass
class Config:
    participantes: List[Participante]
    foo: str

    @staticmethod
    def parse_json(config: Dict[str, Any]) -> 'Config':
        return Config(
            participantes=[
                Participante(nombre=nombre, email=email, excludes=xlist)
                for nombre, (email, xlist) in config['participantes'].items()
            ],
            foo=config['foo'],
        )
