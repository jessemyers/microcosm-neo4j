"""
Neo4J driver factory.

"""
from logging import getLogger, INFO
from microcosm.api import defaults, typed
from microcosm.config.types import boolean

from neo4j.v1 import GraphDatabase


@defaults(
    # NB: some features are not available unless enabled
    enterprise=typed(boolean, default_value=False),
    password="password",
    uri=None,
    username="neo4j",
)
def configure_neo4j_driver(graph):
    if graph.metadata.testing:
        logger = getLogger("neobolt")
        logger.level = INFO

        default_uri = "bolt://localhost:17687"
    else:
        default_uri = "bolt://localhost:7687"

    return GraphDatabase.driver(
        graph.config.neo4j.uri or default_uri,
        auth=(
            graph.config.neo4j.username,
            graph.config.neo4j.password,
        ),
    )
