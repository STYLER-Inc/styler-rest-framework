""" Session management tools
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


_engine = None
_session_local = None


def get_session(database_uri: str) -> Generator:
    global _engine
    global _session_local
    _engine = _engine or create_engine(database_uri, pool_pre_ping=True)
    _session_local = _session_local or sessionmaker(
        autocommit=False, autoflush=False, bind=_engine
    )
    try:
        session_instance = _session_local()
        yield session_instance
    finally:
        session_instance.close()
