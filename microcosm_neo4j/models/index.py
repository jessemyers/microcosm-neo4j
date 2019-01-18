from dataclasses import dataclass


@dataclass(frozen=True)
class Index:
    label: str
    # NB: support for "Node Keys" is not implemented
    key: str
    unique: bool = False

    @classmethod
    def unique(cls, label: str, key: str) -> "Index":
        return cls(label, key)
