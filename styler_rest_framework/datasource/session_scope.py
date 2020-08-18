""" Context manager for a Session scope using Sql Alchemy.

    All functions that reads/writes data to a session in sql alchemy
should use this scope. It handles the initialization and cleanup of a
sql alchemy session within the given engine (connection).
"""

from contextlib import contextmanager

from sqlalchemy import orm


@contextmanager
def create(engine):
    """ Creates a context with a sql alchemy session
    """
    session_maker = orm.sessionmaker(bind=engine)
    session = session_maker()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
