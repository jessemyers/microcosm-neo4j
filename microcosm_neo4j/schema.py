"""
Simplistic management of indexes and constraints.

"""
from neobolt.exceptions import DatabaseError

from microcosm_neo4j.context import SessionContext, transaction
from microcosm_neo4j.errors import (
    Neo4JError,
    NoSuchConstraintError,
    NoSuchIndexError,
)
from microcosm_neo4j.models import Node


class SchemaManager:

    def __init__(self, graph):
        self.graph = graph
        self.query_builder = graph.neo4j_query_builder

    @property
    def session(self):
        return SessionContext.session

    def recreate_all(self):
        """
        Reset the database.

        """
        self.drop_all()
        self.create_all()

    def create_all(self):
        """
        Create the database indexes and constraints.

        See: https://neo4j.com/docs/cypher-manual/current/schema/index/
        See: https://neo4j.com/docs/cypher-manual/current/schema/constraints/

        """
        for model_class, index in self.iter_indexes():
            self.run(self.query_builder.manage_index(model_class, index, drop=False))

    def drop_all(self, force=False):
        """
        Drop the database.

        The technique used here is only suitable for unit tests. Any use case with large numbers
        of nodes should operate at a lower level.

        """
        for model_class, index in self.iter_indexes():
            try:
                self.run(self.query_builder.manage_index(model_class, index, drop=True))
            except (NoSuchConstraintError, NoSuchIndexError):
                pass

        if not self.graph.metadata.testing and not force:
            return

        # NB: deleting nodes does not reset auto increment ids; we should not care.
        # NB: data and constraint operations cannot be in the same transaction
        self.run(self.query_builder.drop_all_nodes())

    def run(self, query):
        """
        Run a schema management query.

        XXX There is much to improve here:
         -  Neo4J has no notion of "if exists" or "if not exists". While we can catch the
            resulting errors for unnecessary/duplicate schema changes, these errors invalidate
            transactions (and therefore must be run in isolated transactions).
         -  Neo4J *does* have APIs for querying existing indexes and constraints. We should
            use these and reconcile the expected schema with the existing one.
         -  Error handling and query execution should be centralized.

        """
        try:
            with transaction():
                self.session.run(str(query))
        except DatabaseError as error:
            if "No such constraint" in error.message:
                raise NoSuchConstraintError(error)
            if "No such INDEX" in error.message:
                raise NoSuchIndexError(error)
            raise Neo4JError(error)

    def iter_indexes(self):
        for model_class in Node.__subclasses__():
            for index in model_class.__indexes__:
                yield model_class, index
