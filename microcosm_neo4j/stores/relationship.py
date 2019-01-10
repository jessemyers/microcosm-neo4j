from microcosm_neo4j.errors import MissingDependencyError
from microcosm_neo4j.stores.base import Store


class RelationshipStore(Store):
    """
    Expose persistence operations using `neo4j-driver`.

    """
    def create(self, relationship):
        """
        Upsert a relationship.

        """
        query = self.query_builder.upsert_relationship(relationship)
        items = list(self._all(query))
        if not items:
            raise MissingDependencyError()

        # XXX unlike CREATE, MERGE may find multiple existing relationships
        item = items[0]
        return self.to_relationship(item)

    def delete(self, identifier):
        query = self.query_builder.delete_relationships(self.model_class, id=str(identifier))
        result = self._run(query)
        return result.summary().counters.relationships_deleted

    def retrieve(self, identifier):
        query = self.query_builder.match_relationships(self.model_class, id=str(identifier))
        item = self._one(query)
        return self.to_relationship(item)

    def count(self, **kwargs):
        # XXX relationship counts are not going to be efficient except under narrow circumstances
        # https://neo4j.com/developer/kb/fast-counts-using-the-count-store/
        query = self.query_builder.count_relationships(self.model_class, **kwargs)
        item = self._one(query)
        return item["count"]

    def search(self, **kwargs):
        query = self.query_builder.match_relationships(self.model_class, **kwargs)
        items = self._all(query)
        return [
            self.to_relationship(item)
            for item in items
        ]

    def to_relationship(self, item):
        """
        Convert a result record to a Relationship model.

        """
        kwargs = self.to_dict(item)
        return self.model_class(
            **kwargs,
        )
