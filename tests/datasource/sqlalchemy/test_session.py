""" Tests for session module
"""
from unittest.mock import patch

from styler_rest_framework.datasource.sqlalchemy import session


class TestGetSession:
    """ Tests for get_session
    """
    @patch('styler_rest_framework.datasource.sqlalchemy.session.sessionmaker')
    @patch('styler_rest_framework.datasource.sqlalchemy.session.create_engine')
    def test_get_session(self, create_engine_mocked, sessionmaker_mocked):
        session_instance = session.get_session('uri')
        next(session_instance)

        create_engine_mocked.assert_called_once()
        sessionmaker_mocked.assert_called_once()
