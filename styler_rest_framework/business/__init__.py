""" Module for business classes
"""

from functools import wraps

from styler_rest_framework.datasource import session_scope


def session_aware(func):
    """ Decorator to wrap the method inside a session aware context.

        It also injects the db_session in the function, necessary to
        control flush, commit, and rollbacks.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with session_scope.create(args[0].db_engine) as db_session:
            try:
                kwargs['db_session'] = db_session
                return func(*args, **kwargs)
            except:  # NOQA
                db_session.close()
                raise
    return wrapper


class BaseBusiness:
    """ Base class for business classes
    """
