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

    def test_count_nodes(self):
        cypher = self.query_builder.count_nodes(Person)
        assert_that(
            str(cypher),
            is_(equal_to(
                "MATCH (node:Person) "
                "RETURN count(node) AS count",
            )),
        )

    def test_count_relationships(self):
        cypher = self.query_builder.count_relationships(IsFriendsWith)
        assert_that(
            str(cypher),
            is_(equal_to(
                "MATCH (in:Person)-[relationship:IsFriendsWith]->(out:Person) "
                "RETURN count(relationship) AS count",
            )),
        )

    def test_match_nodes(self):
        cypher = self.query_builder.match_nodes(Person)
        assert_that(
            str(cypher),
            is_(equal_to(
                "MATCH (node:Person) "
                "RETURN node",
            )),
        )

    def test_match_nodes_by_name(self):
        cypher = self.query_builder.match_nodes(Person, name=self.node.name)
        assert_that(
            str(cypher),
            is_(equal_to(
                "MATCH (node:Person {name: $node_name}) "
                "RETURN node",
            )),
        )
        assert_that(
            dict(cypher),
            is_(equal_to(dict(
                node_name=self.node.name,
            ))),
        )

    def test_match_relationships(self):
        cypher = self.query_builder.match_relationships(IsFriendsWith)
        assert_that(
            str(cypher),
            is_(equal_to(
                "MATCH (in:Person)-[relationship:IsFriendsWith]->(out:Person) "
                "RETURN relationship",
            )),
        )

    def test_upsert_node(self):
        cypher = self.query_builder.upsert_node(self.node)
        assert_that(
            str(cypher),
            is_(equal_to(
                "MERGE (node:Person {name: $node_name}) "
                "SET node.id = $node_id "
                "RETURN node",
            )),
        )
        assert_that(
            dict(cypher),
            is_(equal_to(dict(
                node_id=self.node.id,
                node_name=self.node.name,
            ))),
        )

    def test_upsert_relationship(self):
        cypher = self.query_builder.upsert_relationship(self.relationship)
        assert_that(
            str(cypher),
            is_(equal_to(
                "MATCH (in:Person {id: $in_id}) "
                "MATCH (out:Person {id: $out_id}) "
                "MERGE (in)-[relationship:IsFriendsWith "
                "{in_id: $relationship_in_id, out_id: $relationship_out_id, id: $relationship_id}"
                "]->(out) "
                "RETURN relationship"
            )),
        )
        assert_that(
            dict(cypher),
            is_(equal_to(dict(
                in_id=self.relationship.in_id,
                out_id=self.relationship.out_id,
                relationship_id=self.relationship.id,
                relationship_in_id=self.relationship.in_id,
                relationship_out_id=self.relationship.out_id,
            ))),
        )

    def test_create_index(self):
        assert_that(
            str(self.query_builder.create_index(Person, "name")),
            is_(equal_to(
                "CREATE INDEX ON :`Person`(name)",
            )),
        )

    def test_drop_index(self):
        assert_that(
            str(self.query_builder.drop_index(Person, "name")),
            is_(equal_to(
                "DROP INDEX ON :`Person`(name)",
            )),
        )

    def test_create_unique_constraint(self):
        assert_that(
            str(self.query_builder.create_unique_constraint(Person, "name")),
            is_(equal_to(
                "CREATE CONSTRAINT ON (node:`Person`) ASSERT node.`name` IS UNIQUE",
            )),
        )

    def test_drop_unique_constraint(self):
        assert_that(
            str(self.query_builder.drop_unique_constraint(Person, "name")),
            is_(equal_to(
                "DROP CONSTRAINT ON (node:`Person`) ASSERT node.`name` IS UNIQUE",
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
