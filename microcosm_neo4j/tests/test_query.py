from hamcrest import assert_that, equal_to, is_

from microcosm_neo4j.query import QueryBuilder
from microcosm_neo4j.tests.fixtures import IsFriendsWith, Person


class TestQueryBuilder:

    def setup(self):
        self.query_builder = QueryBuilder(Person)
        self.node = Person(name="name")
        self.left = Person(name="left")
        self.right = Person(name="right")
        self.relationship = IsFriendsWith(
            in_id=self.left.id,
            out_id=self.right.id,
        )

    def test_create_index(self):
        assert_that(
            str(self.query_builder.create_index(Person, "name")),
            is_(equal_to(
                "CREATE INDEX ON :Person(name)",
            )),
        )

    def test_drop_index(self):
        assert_that(
            str(self.query_builder.drop_index(Person, "name")),
            is_(equal_to(
                "DROP INDEX ON :Person(name)",
            )),
        )

    def test_create_unique_constraint(self):
        assert_that(
            str(self.query_builder.create_unique_constraint(Person, "name")),
            is_(equal_to(
                "CREATE CONSTRAINT ON (node:Person) ASSERT node.name IS UNIQUE",
            )),
        )

    def test_drop_unique_constraint(self):
        assert_that(
            str(self.query_builder.drop_unique_constraint(Person, "name")),
            is_(equal_to(
                "DROP CONSTRAINT ON (node:Person) ASSERT node.name IS UNIQUE",
            )),
        )

    def test_drop_all_nodes(self):
        cypher = self.query_builder.drop_all_nodes()
        assert_that(
            str(cypher),
            is_(equal_to(
                "MATCH (node) DETACH DELETE node",
            )),
        )
