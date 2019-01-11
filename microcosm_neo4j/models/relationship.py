from dataclasses import field
from uuid import uuid4

from inflection import underscore

from microcosm_neo4j.models.entity import Entity


class RelationshipMeta(type):

    def __new__(cls, name, bases, dct):
        if name == "Relationship":
            return super().__new__(cls, name, bases + (Entity, ), dct)

        # inject the id's type
        dct["__annotations__"].update(
            id=str,
        )
        # inject the id's default factory
        dct.update(
            id=field(default_factory=lambda: str(uuid4())),
        )
        return super().__new__(cls, name, bases + (Entity,), dct)


class Relationship(metaclass=RelationshipMeta):
    """
    Base class for Neo4J relationships.

    """
    @classmethod
    def label(cls) -> str:
        return underscore(cls.__name__).upper()
