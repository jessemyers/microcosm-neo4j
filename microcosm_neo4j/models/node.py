from dataclasses import field
from typing import Mapping
from uuid import uuid4

from microcosm_neo4j.models.entity import Entity
from microcosm_neo4j.models.index import UniqueIndex
from microcosm_neo4j.models.types import PropertyType


class NodeMeta(type):

    def __new__(cls, name, bases, dct):
        if name == "Node":
            return super().__new__(cls, name, bases + (Entity, ), dct)

        # inject the id's type
        dct["__annotations__"].update(
            id=str,
        )
        # inject the id's default factory
        dct.update(
            id=field(default_factory=lambda: str(uuid4())),
        )

        dct.setdefault("__indexes__", []).append(
            UniqueIndex("id"),
        )

        return super().__new__(cls, name, bases, dct)


class Node(metaclass=NodeMeta):
    """
    Base class for Neo4J nodes.

    """
    def unique_properties(self) -> Mapping[str, PropertyType]:
        keys = {
            index.name
            for index in getattr(self, "__indexes__")
            if index.unique and index.name != "id"
        }
        return {
            key: value
            for key, value in getattr(self, "properties")().items()
            if key in keys
        }

    def value_properties(self) -> Mapping[str, PropertyType]:
        """
        Return the identity properties of this entity

        """
        keys = {
            index.name
            for index in getattr(self, "__indexes__")
            if index.unique and index.name != "id"
        }
        return {
            key: value
            for key, value in getattr(self, "properties")().items()
            if key not in keys
        }
