""" Paginator
"""

from math import ceil


class InvalidParameterError(ValueError):
    """ Raised when page or limit is invalid
    """


class Paginator:
    """ Handles pagination
    """

    def __init__(self, limit=20, page=1):
        try:
            if not page:
                page = 1
            self._current = int(page)
        except ValueError:
            raise InvalidParameterError('Invalid page')

        try:
            if not limit:
                limit = 20
            self._limit = int(limit)
        except ValueError:
            raise InvalidParameterError('Invalid limit')

        if self._current < 1:
            raise InvalidParameterError('Invalid page')
        if self._limit < 1:
            raise InvalidParameterError('Invalid limit')

        self._count = None
        self._total_pages = None

    def get_page(self, query):
        """ Retrieve a page of items

            Args:
                query: query object
            Returns:
                A list of items within the boundaries set by the pagination
        """
        self._count = query.count()
        self._total_pages = int(ceil(self._count / float(self._limit)))
        offset = (self._current - 1) * self._limit
        if self._total_pages > 0 and self._current > self._total_pages:
            raise InvalidParameterError('Invalid page')
        return query.offset(offset).limit(self._limit).all()

    def get_info(self):
        """ Retrieves information about the pagination status
        """
        nex_page = (
            self._current + 1
            if self._current < self._total_pages
            else None
        )
        return {
            'total_pages': self._total_pages,
            'total_number_of_items': self._count,
            'current_page': self._current,
            'previous_page': self._current - 1 if self._current > 1 else None,
            'next_page': nex_page
        }
