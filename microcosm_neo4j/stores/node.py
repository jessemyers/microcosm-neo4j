from microcosm_neo4j.stores.base import Store


class NodeStore(Store):
    """
    Expose node persistence operations using `neo4j-driver`.

    """
    def create(self, node):
        query = self.query_builder.upsert_node(node, "n")
        item = self._one(query)
        return self.model_class(**self.to_dict(item))

    def delete(self, identifier):
        query = self.query_builder.delete_nodes(self.model_class, id=str(identifier))
        result = self._run(query)
        return result.summary().counters.nodes_deleted

    def retrieve(self, identifier):
        query = self.query_builder.match_nodes(self.model_class, id=str(identifier))
        item = self._one(query)
        return self.model_class(**self.to_dict(item))

    def search(self, **kwargs):
        query = self.query_builder.match_nodes(self.model_class, **kwargs)
        items = self._all(query)
        # XXX support offset+limit (via skip/limit)
        return [
            self.model_class(**self.to_dict(item))
            for item in items
        ]

    def count(self, **kwargs):
        # XXX count may not be efficient
        # https://neo4j.com/developer/kb/fast-counts-using-the-count-store/
        query = self.query_builder.count_nodes(self.model_class, **kwargs)
        item = self._one(query)
        return item["count"]
