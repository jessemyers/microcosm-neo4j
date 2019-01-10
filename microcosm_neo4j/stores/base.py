from contextlib import contextmanager

from neobolt.exceptions import ConstraintError
from opencypher.ast import Cypher

from microcosm_neo4j.context import SessionContext
from microcosm_neo4j.errors import (
    DuplicateModelError,
    ModelIntegrityError,
    NotFoundError,
)


class Store:
    def __init__(self, graph, model_class):
        self.graph = graph
        self.model_class = model_class
        self.query_builder = graph.neo4j_query_builder

    @property
    def session(self):
        return SessionContext.session

    def _one(self, query):
        with self.error_handling():
            return self._run(query).single()

    def _all(self, query):
        with self.error_handling():
            return self._run(query)

    def _run(self, query: Cypher):
        """
        Run a query using the current session.

        """
        # express the query as a string
        cypher = str(query)
        # express the parameters as a dictionary
        parameters = dict(query)
        return self.session.run(cypher, **parameters)

    @contextmanager
    def error_handling(self):
        try:
            yield
        except ConstraintError as error:
            if "already exists" in error.message:
                raise DuplicateModelError(error)
            if "due to conflicts with existing unique nodes" in error.message:
                raise DuplicateModelError(error)
            raise ModelIntegrityError(error)

    def to_dict(self, record):
        """
        Convert a return value into a dictionary.

        Note that while the `_id` property is accessible during this translation,
        we choose to respect Neo4J's design that its internal integer ids be treated
        as implementation details.

        """
        if record is None:
            # Neo4J doesn't give us a lot of context in its error responses; however just about
            # every reason we might not get back a result relates to either omitting a `RETURN`
            # clause or defining `MATCH` clause with no results.
            raise NotFoundError()

        # NB: assumes we only want one record at a time; for more complex cases use `record[variable]`
        entity = next(iter(record))
        return entity._properties
