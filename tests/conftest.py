""" Conftest
"""

import pytest


@pytest.fixture
def event_loop(loop):
    return loop
