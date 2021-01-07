from unittest.mock import Mock
from styler_rest_framework.crud.base import CRUDBase


class TestCRUDbase:
    """ Test CRUD base
    """
    def test_get(self):
        """ It should call related function
        """
        db = Mock()
        model = Mock()

        base = CRUDBase(model)

        base.get(db, 'test_id')

        db.query.assert_called_once()

    def test_get_multi(self):
        """ It should call related function
        """
        db = Mock()
        model = Mock()

        base = CRUDBase(model)

        base.get_multi(db)

        db.query.assert_called_once()

    def test_create(self):
        """ It should call related function
        """
        db = Mock()
        model = Mock()

        base = CRUDBase(model)

        base.create(db, obj_in={'key': 'value'})

        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()

    def test_update(self):
        """ It should call related function
        """
        db = Mock()
        model = Mock()

        base = CRUDBase(model)

        base.update(db, db_obj=Mock(), obj_in={'key': 'value'})

        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()

    def test_remove(self):
        """ It should call related function
        """
        db = Mock()
        model = Mock()

        base = CRUDBase(model)

        base.remove(db, id='test_id')

        db.query.assert_called_once()
        db.delete.assert_called_once()
        db.commit.assert_called_once()
