from hamcrest import (
    assert_that,
    calling,
    has_length,
    raises,
)
from microcosm.api import create_object_graph

from microcosm_neo4j.context import SessionContext
from microcosm_neo4j.errors import (
    MissingDependencyError,
)
from microcosm_neo4j.tests.fixtures import (
    IsFriendsWith,
    Person,
    PersonStore,
    IsFriendsWithStore,
)


class TestRelationshipStore:

    def setup(self):
        self.graph = create_object_graph("microcosm_neo4j", testing=True)
        self.person_store = PersonStore(self.graph)
        self.store = IsFriendsWithStore(self.graph)

        with SessionContext(self.graph) as context:
            context.recreate_all()

        self.left = Person(name="left")
        self.right = Person(name="right")

        self.relationship = IsFriendsWith(
            in_id=self.left.id,
            out_id=self.right.id,
        )

    def test_create(self):
        with SessionContext(self.graph):
            self.person_store.create(self.left)
            self.person_store.create(self.right)
            self.store.create(self.relationship)

    def test_create_with_missing_dependency(self):
        with SessionContext(self.graph):
            self.person_store.create(self.left)
            assert_that(
                calling(self.store.create).with_args(self.relationship),
                raises(MissingDependencyError),
            )

    def test_search(self):
        with SessionContext(self.graph):
            self.person_store.create(self.left)
            self.person_store.create(self.right)
            self.store.create(self.relationship)

            assert_that(
                self.store.search(),
                has_length(1),
            )

    def test_upsert_search(self):
        with SessionContext(self.graph):
            self.person_store.create(self.left)
            self.person_store.create(self.right)
            self.store.create(self.relationship)
            self.store.create(self.relationship)
            assert_that(
                self.store.search(),
                has_length(1),
            )
