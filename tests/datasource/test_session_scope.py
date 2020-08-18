""" Tests for session scope
"""

from unittest.mock import Mock, patch

from styler_rest_framework.datasource import session_scope
import pytest


class MySession:
    """ Represents a mock session
    """
    rollback = Mock()
    close = Mock()


@patch('sqlalchemy.orm.sessionmaker', Mock(return_value=MySession))
def test_session_in_context():
    with pytest.raises(ValueError):
        with session_scope.create(Mock()) as session:
            some_op = Mock(side_effect=ValueError('something wrong'))
            some_op()
    session.rollback.assert_called_once()
    session.close.assert_called_once()
