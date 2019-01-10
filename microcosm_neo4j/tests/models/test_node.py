from hamcrest import (
    assert_that,
    contains_inanyorder,
    has_entries,
)

from microcosm_neo4j.tests.fixtures import Person


class TestNode:

    def setup(self):
        self.nodes = [
            Person(name="left"),
            Person(name="right"),
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
