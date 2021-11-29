"""Tests for Firestore Handler
"""
import pytest

from styler_rest_framework.datasource import Datasource

DATA_ROOT_PATH = "firestore-test/v1/data"


class TestSaveDocument:
    """Tests for function save_document"""

    def test_normal_flow(self, mock_db):
        """Tests normal flow for function save_document"""
        mock_db.reset()
        test_data = Datasource()
        test_doc = {"test_key": "test_value"}
        test_doc_id = "test_doc_1"
        test_data.save_document(
            mock_db,
            DATA_ROOT_PATH,
            test_doc,
            test_doc_id,
        )

        doc_content = (
            mock_db.document(f"{DATA_ROOT_PATH}/{test_doc_id}").get().to_dict()
        )

        assert doc_content == test_doc


class TestSaveDocument:
    """Tests for function all_documents"""

    def test_normal_flow(self, mock_db, with_firestore_docs):
        """Tests normal flow for function save_document"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        result = test_data.all_documents(mock_db, DATA_ROOT_PATH)
        assert len(result) == doc_count
        for i, doc in enumerate(result):
            assert doc == test_docs[i]


class TestQueryWithArguments:
    """Tests for function query_with_arguments"""

    def test_single_where_object(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        where_list = [{"field_path": "number", "op_string": ">", "value": 5}]
        result = test_data.query_with_arguments(
            mock_db, DATA_ROOT_PATH, where=where_list
        )
        assert len(result) == 5
        for i, doc in enumerate(result):
            assert doc == test_docs[i + 5]

    def test_multiple_where_object(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        where_list = [
            {"field_path": "number", "op_string": ">", "value": 5},
            {"field_path": "number", "op_string": "<", "value": 8},
        ]
        result = test_data.query_with_arguments(
            mock_db, DATA_ROOT_PATH, where=where_list
        )
        assert len(result) == 2
        assert result[0] == test_docs[5]
        assert result[1] == test_docs[6]

    def test_invalid_where_object_type(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        where_list = {"field_path": "number", "op_string": ">", "value": 5}
        with pytest.raises(ValueError) as expected:
            test_data.query_with_arguments(mock_db, DATA_ROOT_PATH, where=where_list)
            assert expected.value.errors == "where argument should be a list!"

    def test_invalid_key_in_where_object(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        where_list = [{"invalid_key": "number"}]
        with pytest.raises(ValueError) as expected:
            test_data.query_with_arguments(mock_db, DATA_ROOT_PATH, where=where_list)
            assert (
                expected.value.errors
                == 'where object must contain "field_path", "op_string" and "value" fields!'
            )

    def test_with_order_by_alone(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        order_by = {"field_path": "number", "direction": "DESCENDING"}
        result = test_data.query_with_arguments(
            mock_db, DATA_ROOT_PATH, order_by=order_by
        )
        assert len(result) == 10
        assert result[0] == test_docs[-1]
        assert result[-1] == test_docs[0]

    def test_with_both_where_and_order_by(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        where_list = [
            {"field_path": "nest_dict.number", "op_string": ">", "value": 5},
            {"field_path": "nest_dict.number", "op_string": "<", "value": 8},
        ]
        order_by = {"field_path": "number"}
        result = test_data.query_with_arguments(
            mock_db, DATA_ROOT_PATH, where=where_list, order_by=order_by
        )
        assert len(result) == 2
        assert result[0] == test_docs[5]
        assert result[1] == test_docs[6]

    def test_invalid_order_by_type(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        order_by = [{"field_path": "number", "direction": "DESCENDING"}]

        with pytest.raises(ValueError) as expected:
            test_data.query_with_arguments(mock_db, DATA_ROOT_PATH, order_by=order_by)
            assert expected.value.errors == "order_by argument should be a dictionary!"

    def test_invalid_order_by_key(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        order_by = {"direction": "DESCENDING"}

        with pytest.raises(ValueError) as expected:
            test_data.query_with_arguments(mock_db, DATA_ROOT_PATH, order_by=order_by)
            assert expected.value.errors == "invalid order_by argument!"

    def test_invalid_direction_in_order_by(self, mock_db, with_firestore_docs):
        """Tests normal flow for function query_with_arguments"""
        mock_db.reset()
        doc_count = 10
        test_docs = with_firestore_docs(DATA_ROOT_PATH, doc_count=doc_count)
        test_data = Datasource()
        order_by = [{"field_path": "number", "direction": "invalid"}]

        with pytest.raises(ValueError) as expected:
            test_data.query_with_arguments(mock_db, DATA_ROOT_PATH, order_by=order_by)
            assert expected.value.errors == 'direction of order_by must be "ASCENDING" or "DESCENDING"!'
