from dataclasses import dataclass, field
from typing import List


@dataclass
class Index:
    name: str
    unique: bool = False
    targets: List[str] = field(default_factory=list)


class UniqueIndex(Index):
    def __init__(self, name: str):
        super().__init__(name, True)
