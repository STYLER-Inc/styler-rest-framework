""" Tests for the session aware decorator
"""

from contextlib import contextmanager
from unittest.mock import Mock, patch

from styler_rest_framework.business import session_aware
import pytest


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


def mock_session2(m):
    @contextmanager
    def create(engine):
        yield m
    return create


def test_close():
    @session_aware
    def mock_func(obj, db_session=None):
        raise ValueError()
    my_business = Mock()
    my_business.db_engine = Mock()
    mocked = Mock()
    with patch(
        'styler_rest_framework.datasource.session_scope.create',
        mock_session2(mocked)
    ):
        with pytest.raises(ValueError):
            _ = mock_func(my_business)

    mocked.close.assert_called_once()
