from dataclasses import dataclass
from typing import Type

from hamcrest import has_properties

from microcosm_neo4j.models import Node, Relationship, Index
from microcosm_neo4j.stores import NodeStore, RelationshipStore


@dataclass(frozen=False)
class Person(Node):
    name: str

    __indexes__ = [
        Index("Person", "name"),
    ]


@dataclass(frozen=False)
class IsFriendsWith(Relationship):

    @classmethod
    def in_class(cls) -> Type[Person]:
        return Person

    @classmethod
    def out_class(cls) -> Type[Person]:
        return Person


class PersonStore(NodeStore[Person]):

    def __init__(self, graph):
        super().__init__(graph, Person)


class IsFriendsWithStore(RelationshipStore[IsFriendsWith]):

    def __init__(self, graph):
        super().__init__(graph, IsFriendsWith)


def matches_person(person):
    return has_properties(
        name=person.name,
    )
