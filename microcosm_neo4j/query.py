from opencypher.api import (
    func,
    expr,
    match,
    merge,
    node,
    parameters,
)


class QueryBuilder:
    """
    Build queries using Pypher.

    """
    def __init__(self, graph):
        pass

    def count_nodes(self, model_class, variable="node", **kwargs):
        return match(
            node(
                variable,
                model_class.label(),
                properties=model_class.matching_properties(**kwargs),
            ),
        ).ret(
            func.count(variable).as_("count"),
        )

    def delete_nodes(self, model_class, variable="node", **kwargs):
        return match(
            node(
                variable,
                model_class.label(),
                properties=model_class.matching_properties(**kwargs),
            ),
        ).delete(
            variable,
        )

    def match_nodes(self, model_class, variable="node", **kwargs):
        return match(
            node(
                variable,
                model_class.label(),
                properties=model_class.matching_properties(**kwargs),
            ),
        ).ret(
            expr(variable),
        )

    def upsert_node(self, model, variable="node"):
        assignments = parameters(
            key_prefix=variable,
            name_prefix=variable,
            **model.value_properties()
        )
        return merge(
            node(
                variable,
                model.__class__.label(),
                properties=model.unique_properties(),
            ),
        ).set(
            assignments[0],
            *assignments[1:],
        ).ret(
            expr(variable),
        )

    def upsert_relationship(self, model, variable="relationship"):
        return match(
            node(
                "in",
                model.in_class.label(),
                properties=dict(
                    id=model.in_id,
                ),
            ),
        ).match(
            node(
                "out",
                model.out_class.label(),
                properties=dict(
                    id=model.out_id,
                ),
            ),
        ).merge(
            node(
                "in",
            ).rel_in(
                variable,
                model.__class__.label(),
                properties=model.properties(),
            ).node(
                "out",
            ),
        ).ret(
            expr(variable),
        )

    def count_relationships(self, model_class, variable="relationship", **kwargs):
        # XXX count performance for relationships is probably going to be bad
        #
        # Just about any property-based matching means we won't use the count indexes.
        # Just about any node-label-based matching means the same. We may wish to avoid such
        # things by minimizing relationship polymorphism.
        return match(
            node(
                "in",
                model_class.in_class.label(),
            ).rel_in(
                variable,
                model_class.label(),
                properties=model_class.matching_properties(**kwargs),
            ).node(
                "out",
                model_class.out_class.label(),
            ),
        ).ret(
            func.count(variable).as_("count"),
        )

    def match_relationships(self, model_class, variable="relationship", **kwargs):
        return match(
            node(
                "in",
                model_class.in_class.label(),
            ).rel_in(
                variable,
                model_class.label(),
                properties=model_class.matching_properties(**kwargs),
            ).node(
                "out",
                model_class.out_class.label(),
            ),
        ).ret(
            variable,
        )

    def delete_relationships(self, model_class, variable="node", **kwargs):
        return match(
            node(
                "in",
                model_class.in_class.label(),
            ).rel_in(
                variable,
                model_class.label(),
                properties=model_class.matching_properties(**kwargs),
            ).node(
                "out",
                model_class.out_class.label(),
            ),
        ).delete(
            variable,
        )

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
        return f"CREATE INDEX ON :`{model_class.label()}`({key})"

    def drop_index(self, model_class, key):
        return f"DROP INDEX ON :`{model_class.label()}`({key})"

    def create_unique_constraint(self, model_class, key):
        return f"CREATE CONSTRAINT ON (node:`{model_class.label()}`) ASSERT node.`{key}` IS UNIQUE"

    def drop_unique_constraint(self, model_class, key):
        return f"DROP CONSTRAINT ON (node:`{model_class.label()}`) ASSERT node.`{key}` IS UNIQUE"

    def drop_all_nodes(self):
        return match(
            node("node"),
        ).delete(
            "node",
            detach=True,
        )
