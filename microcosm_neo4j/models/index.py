from dataclasses import dataclass


@dataclass
class Index:
    name: str
    unique: bool = False


class UniqueIndex(Index):
    def __init__(self, name: str):
        super().__init__(name, True)
