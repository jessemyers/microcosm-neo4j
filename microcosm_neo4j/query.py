from opencypher.api import (
    match,
    node,
)


class QueryBuilder:
    """
    Build queries using Pypher.

    """
    def __init__(self, graph):
        pass

    def manage_index(self, model_class, index, drop=False):
        # NB: uniqueness constraints imply an index
        if drop:
            if index.unique:
                return self.drop_unique_constraint(model_class, index.name)
            else:
                return self.drop_index(model_class, index.name)
        else:
            if index.unique:
                return self.create_unique_constraint(model_class, index.name)
            else:
                return self.create_index(model_class, index.name)

    def create_index(self, model_class, key):
        return f"CREATE INDEX ON :{model_class.label()}({key})"

    def drop_index(self, model_class, key):
        return f"DROP INDEX ON :{model_class.label()}({key})"

    def create_unique_constraint(self, model_class, key):
        return f"CREATE CONSTRAINT ON (node:{model_class.label()}) ASSERT node.{key} IS UNIQUE"

    def drop_unique_constraint(self, model_class, key):
        return f"DROP CONSTRAINT ON (node:{model_class.label()}) ASSERT node.{key} IS UNIQUE"

    def drop_all_nodes(self):
        return match(
            node("node"),
        ).delete(
            "node",
            detach=True,
        )
