from dataclasses import field
from typing import Mapping
from uuid import uuid4

from inflection import camelize

from microcosm_neo4j.models.entity import Entity
from microcosm_neo4j.models.index import Index
from microcosm_neo4j.models.types import PropertyType


class NodeMeta(type):

    def __new__(cls, name, bases, dct):
        if name == "Node":
            return super().__new__(cls, name, bases, dct)

        # inject the id's type
        dct.setdefault("__annotations__", {}).update(
            id=str,
        )
        # inject the id's default factory
        dct.update(
            id=field(default_factory=lambda: str(uuid4())),
        )

        dct.setdefault("__indexes__", []).append(
            Index.unique(name, "id"),
        )

        return super().__new__(cls, name, bases, dct)


class Node(Entity, metaclass=NodeMeta):
    """
    Base class for Neo4J nodes.

    """
    def unique_properties(self) -> Mapping[str, PropertyType]:
        keys = {
            index.key
            for index in getattr(self, "__indexes__")
            if index.unique and "id" != index.key
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
            index.key
            for index in getattr(self, "__indexes__")
            if index.unique and "id" != index.key
        }
        return {
            key: value
            for key, value in getattr(self, "properties")().items()
            if key not in keys
        }

    @classmethod
    def label(cls) -> str:
        return camelize(cls.__name__)
