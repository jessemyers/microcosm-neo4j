from hamcrest import (
    assert_that,
    contains_inanyorder,
    has_entries,
)

from microcosm_neo4j.tests.fixtures import Person, IsFriendsWith


class TestModel:

    def setup(self):
        self.nodes = [
            Person(name="left"),
            Person(name="right"),
        ]
        self.relationships = [
            IsFriendsWith(
                in_id=self.nodes[0].id,
                out_id=self.nodes[1].id,
            ),
        ]

    def test_node_properties(self):
        assert_that(
            self.nodes[0].properties(),
            has_entries(
                name="left",
            ),
        )

    def test_node_property_names(self):
        assert_that(
            Person.property_names(),
            contains_inanyorder(
                "id",
                "name",
            ),
        )

    def test_relationship_properties(self):
        assert_that(
            self.relationships[0].properties(),
            has_entries(
                in_id=self.nodes[0].id,
                out_id=self.nodes[1].id,
            ),
        )

    def test_relationship_property_names(self):
        assert_that(
            IsFriendsWith.property_names(),
            contains_inanyorder(
                "id",
                "in_id",
                "out_id",
            ),
        )
