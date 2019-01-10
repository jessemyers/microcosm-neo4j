from hamcrest import (
    assert_that,
    calling,
    contains,
    contains_inanyorder,
    equal_to,
    has_length,
    is_,
    raises,
)
from microcosm.api import create_object_graph

from microcosm_neo4j.context import SessionContext
from microcosm_neo4j.errors import (
    MissingDependencyError,
)
from microcosm_neo4j.tests.fixtures import (
    matches_person,
    IsFriendsWith,
    Person,
    PersonStore,
    IsFriendsWithStore,
)


class TestNodeStore:

    def setup(self):
        self.graph = create_object_graph("microcosm_neo4j", testing=True)
        self.store = PersonStore(self.graph)

        with SessionContext(self.graph) as context:
            context.recreate_all()

        self.node = Person(name="name")

    def test_create(self):
        with SessionContext(self.graph):
            assert_that(
                self.store.create(self.node),
                matches_person(self.node),
            )

    def test_upsert(self):
        with SessionContext(self.graph):
            self.store.create(self.node)

            assert_that(
                self.store.create(self.node),
                matches_person(self.node),
            )

            assert_that(
                self.store.count(),
                is_(equal_to(1)),
            )

    def test_count(self):
        with SessionContext(self.graph):
            self.store.create(self.node)

            assert_that(
                self.store.count(),
                is_(equal_to(1)),
            )

    def test_search(self):
        with SessionContext(self.graph):
            self.store.create(self.node)

            assert_that(
                self.store.search(),
                contains(
                    matches_person(self.node),
                ),
            )

    def test_search_filter(self):
        other = Person(name="other")
        with SessionContext(self.graph):
            self.store.create(self.node)
            self.store.create(other)

            assert_that(
                self.store.search(),
                contains_inanyorder(
                    matches_person(self.node),
                    matches_person(other),
                ),
            )

            assert_that(
                self.store.search(name=self.node.name),
                contains(
                    matches_person(self.node),
                ),
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
