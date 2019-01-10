"""
Test Neo4J driver factory.

"""
from hamcrest import assert_that, is_not, none
from microcosm.api import create_object_graph


def test_create_neo4j_driver():
    graph = create_object_graph("microcosm_neo4j", testing=True)
    assert_that(graph.neo4j, is_not(none()))
