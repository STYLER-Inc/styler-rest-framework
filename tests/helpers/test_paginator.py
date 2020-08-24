""" Tests for the Paginator
"""

import pytest
from unittest.mock import Mock, call

from styler_rest_framework.helpers.paginator import \
    Paginator, InvalidParameterError


class TestInit:
    """ Tests for constructor
    """
    def test_init_a_paginator(self):
        pag = Paginator(limit=10, page=1)

        assert isinstance(pag, Paginator)

    def test_init_a_paginator_with_none(self):
        pag = Paginator(limit=None, page=None)

        assert isinstance(pag, Paginator)
        assert pag._current == 1
        assert pag._limit == 20

    def test_invalid_limit(self):
        with pytest.raises(InvalidParameterError) as expected:
            Paginator(limit=-1, page=1)
        assert str(expected.value) == 'Invalid limit'

    def test_invalid_limit_type(self):
        with pytest.raises(InvalidParameterError) as expected:
            Paginator(limit='aaa', page=1)
        assert str(expected.value) == 'Invalid limit'

    def test_invalid_page(self):
        with pytest.raises(InvalidParameterError) as expected:
            Paginator(limit=10, page=-1)
        assert str(expected.value) == 'Invalid page'

    def test_invalid_page_type(self):
        with pytest.raises(InvalidParameterError) as expected:
            Paginator(limit=10, page='aaa')
        assert str(expected.value) == 'Invalid page'


class TestGetPage:
    """ Tests for get_page
    """
    def test_normal_flow(self):
        """ It should return the item page without errors
        """
        query = Mock()
        query.count.return_value = 100
        query.offset.return_value = query
        query.limit.return_value = query
        query.all.return_value = [1, 2, 3]
        pag = Paginator(limit=10, page=1)

        result = pag.get_page(query)

        assert result == [1, 2, 3]
        assert query.count.call_count == 1
        assert call(0) in query.offset.mock_calls
        assert call(10) in query.limit.mock_calls

    def test_invalid_page(self):
        """ It should raise an exception
        """
        query = Mock()
        query.count.return_value = 5
        query.offset.return_value = query
        query.limit.return_value = query
        query.all.return_value = [1, 2, 3]
        pag = Paginator(limit=10, page=2)

        with pytest.raises(InvalidParameterError) as expected:
            _ = pag.get_page(query)

        assert str(expected.value) == 'Invalid page'
        assert query.count.call_count == 1
        assert query.offset.call_count == 0
        assert query.limit.call_count == 0


class TestGetInfo:
    """ Tests for get_info
    """
    def test_get_info(self):
        query = Mock()
        query.count.return_value = 100
        query.offset.return_value = query
        query.limit.return_value = query
        query.all.return_value = [1, 2, 3]
        pag = Paginator(limit=10, page=3)

        pag.get_page(query)
        info = pag.get_info()

        assert info['total_pages'] == 10
        assert info['total_number_of_items'] == 100
        assert info['current_page'] == 3
        assert info['previous_page'] == 2
        assert info['next_page'] == 4

    def test_none_previous_page(self):
        """ Should return None in the previous page if current page == 1
        """
        query = Mock()
        query.count.return_value = 100
        query.offset.return_value = query
        query.limit.return_value = query
        query.all.return_value = [1, 2, 3]
        pag = Paginator(limit=10, page=1)

        pag.get_page(query)
        info = pag.get_info()

        assert info['total_pages'] == 10
        assert info['total_number_of_items'] == 100
        assert info['current_page'] == 1
        assert info['previous_page'] is None
        assert info['next_page'] == 2

    def test_none_next_page(self):
        """ Should return None in the next page if current page == total_pages
        """
        query = Mock()
        query.count.return_value = 100
        query.offset.return_value = query
        query.limit.return_value = query
        query.all.return_value = [1, 2, 3]
        pag = Paginator(limit=10, page=10)

        pag.get_page(query)
        info = pag.get_info()

        assert info['total_pages'] == 10
        assert info['total_number_of_items'] == 100
        assert info['current_page'] == 10
        assert info['previous_page'] == 9
        assert info['next_page'] is None
