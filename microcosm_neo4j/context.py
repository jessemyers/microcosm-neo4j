"""
Session context management.

"""
from contextlib import contextmanager
from functools import wraps


class SessionContext:
    """
    Save current session in well-known location and provide context management.

    """
    session = None

    def __init__(self, graph):
        self.graph = graph

    def open(self):
        """
        Create a new session and transaction.

        Always run in transactional mode; otherwise the session will auto-commit.

        """
        SessionContext.session = self.graph.neo4j.session()
        SessionContext.session.begin_transaction()
        return self

    def close(self):
        """
        Close the session.

        Without `transaction`, closing will rollback writes.

        """
        if SessionContext.session:
            SessionContext.session.close()
            SessionContext.session = None

    # session factory

    @classmethod
    def make(cls, graph):
        return cls(graph).open()

    # unit test shortcut

    def recreate_all(self):
        self.graph.neo4j_schema_manager.recreate_all()

    # context manager

    def __enter__(self):
        return self.open()

    def __exit__(self, *args, **kwargs):
        self.close()


@contextmanager
def transaction():
    """
    Wrap a context with a commit/rollback.

    """
    try:
        # NB: In the local Flask development server, using per-process session state is unsafe.
        # Concurrent session operations may interleave and reset the session reference.
        assert SessionContext.session, "No Neo4J session: check your concurrency"
        if not SessionContext.session.has_transaction():
            SessionContext.session.begin_transaction()
        yield SessionContext.session
        SessionContext.session.commit_transaction()
    except Exception:
        if SessionContext.session and SessionContext.session.has_transaction():
            SessionContext.session.rollback_transaction()
        raise


def transactional(func):
    """
    Decorate a function call with a commit/rollback and pass the session as the first arg.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction():
            return func(*args, **kwargs)
    return wrapper
