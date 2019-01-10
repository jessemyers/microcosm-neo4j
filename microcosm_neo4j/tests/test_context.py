"""
Test session context management.

"""
from hamcrest import (
    assert_that,
    contains,
    empty,
    is_,
)
from microcosm.api import create_object_graph

from microcosm_neo4j.context import SessionContext, transaction
from microcosm_neo4j.tests.fixtures import matches_person, Person, PersonStore


class Break(Exception):
    pass


class TestSessionContext:

    def setup(self):
        self.graph = create_object_graph("microcosm_neo4j", testing=True)
        self.store = PersonStore(self.graph)

        with SessionContext(self.graph) as context:
            context.recreate_all()

        self.name = "Steph Curry"
        self.person = Person(name=self.name)

    def test_transaction_commit(self):
        """
        Explicit transactions persist across sessions.

        """
        with SessionContext(self.graph), transaction():
            self.store.create(self.person)

        with SessionContext(self.graph):
            people = self.store.search(name=self.name)

        assert_that(
            people,
            contains(
                matches_person(self.person),
            ),
        )

    def test_transaction_rollback_on_error(self):
        """
        Errors raised during a transaction cause a rollback.

        """
        with SessionContext(self.graph):
            try:
                with transaction():
                    self.store.create(self.person)

                    raise Break()
            except Break:
                pass

        with SessionContext(self.graph):
            people = self.store.search(name=self.name)

        assert_that(people, is_(empty()))

    def test_auto_rollback(self):
        """
        Sessions created without explicit transactions automatically rollback.

        """
        with SessionContext(self.graph):
            self.store.create(self.person)

        with SessionContext(self.graph):
            people = self.store.search(name=self.name)

        assert_that(
            people,
            is_(empty()),
        )
