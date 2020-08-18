""" Tests for the session aware decorator
"""

from contextlib import contextmanager
from unittest.mock import Mock, patch

from styler_rest_framework.business import session_aware


@contextmanager
def mock_session(engine):
    yield 'db session'


@patch('styler_rest_framework.datasource.session_scope.create', mock_session)
def test_session_aware():
    @session_aware
    def mock_func(obj, db_session=None):
        return db_session
    my_business = Mock()
    my_business.db_engine = Mock()

    result = mock_func(my_business)

    assert result == 'db session'
