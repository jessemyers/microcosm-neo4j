from dataclasses import dataclass

from hamcrest import has_properties

from microcosm_neo4j.models import Node, Relationship, UniqueIndex
from microcosm_neo4j.stores import NodeStore, RelationshipStore


@dataclass(frozen=False)
class Person(Node):
    name: str

    __indexes__ = [
        UniqueIndex("name"),
    ]


@dataclass(frozen=False)
class IsFriendsWith(Relationship):
    in_id: str
    out_id: str

    in_class = Person
    out_class = Person


class PersonStore(NodeStore):
    def __init__(self, graph):
        super().__init__(graph, Person)


class IsFriendsWithStore(RelationshipStore):
    def __init__(self, graph):
        super().__init__(graph, IsFriendsWith)


def matches_person(person):
    return has_properties(
        name=person.name,
    )
