from typing import Dict, List


class Datasource:
    def all_documents(self, db, path: str):
        query = db.collection(path)
        return [doc.to_dict() for doc in query.stream()]

    def save_document(self, db, path: str, doc, doc_id):
        return db.document(f"{path}/{doc_id}").set(doc)

    def query_with_arguments(
        self, db, path: str, where: List = None, order_by: Dict = None
    ):
        """Perform simple and compound queries in Firestore

        :param db: Firestore client
        :type db: Firestore client
        :param path: path to the collection
        :type path: str
        :param where: A list of where object, which is a Dict must contain the following content:
            * field_path (str) – A field path (.-delimited list of field names) for the field to filter on.
            * op_string (str) – A comparison operation in the form of a string. Acceptable values are <, <=, ==, !=, >=, >, in, not-in, array_contains and array_contains_any.
            * value (Any) – The value to compare the field against in the filter. If value is None or a NaN, then == is the only allowed operation.
            Query for firestore has some limitations, please check https://firebase.google.com/docs/firestore/query-data/queries#query_limitations for more information.
        :type where: List, optional
        :param order_by: A Dict of order_by object, which should contain the following content:
            * field_path (str) – A field path (.-delimited list of field names) on which to order the query results.
            * direction (Optional[str]) – The direction to order by. Must be one of ASCENDING or DESCENDING, defaults to ASCENDING.
        :type order_by: Dict, optional
        """
        query = db.collection(path)
        if where:
            if not isinstance(where, list):
                raise ValueError("where argument should be a list!")
            for obj in where:
                if "field_path" in obj and "op_string" in obj and "value" in obj:
                    query = query.where(
                        obj["field_path"], obj["op_string"], obj["value"]
                    )
                else:
                    raise ValueError(
                        'where object must contain "field_path", "op_string" and "value" fields!'
                    )
        if order_by:
            if not isinstance(order_by, dict):
                raise ValueError("order_by argument should be a dictionary!")
            if "field_path" in order_by and "direction" in order_by:
                if order_by["direction"] not in ("ASCENDING", "DESCENDING"):
                    raise ValueError(
                        'direction of order_by must be "ASCENDING" or "DESCENDING"!'
                    )
                else:
                    query = query.order_by(
                        order_by["field_path"], order_by["direction"]
                    )
            elif "field_path" in order_by:
                query = query.order_by(order_by["field_path"])
            else:
                raise ValueError("invalid order_by argument!")
        return [doc.to_dict() for doc in query.stream()]
