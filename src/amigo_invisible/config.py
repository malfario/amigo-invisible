from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class Config:
    foo: str


def parse_json(config: Dict[str, Any]) -> Config:
    return Config(
        foo=config['foo'],
    )
