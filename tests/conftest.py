""" Conftest
"""

import pytest
import jwt

from styler_rest_framework.datasource import firestore


@pytest.fixture
def event_loop(loop):
    return loop


@pytest.fixture
def token():
    def generate(
        overwrites=None,
        sysadmin=False,
        admin=False,
        staff=False,
        shops=None,
        organizations=None,
        user_id=None,
    ):
        if overwrites is None:
            overwrites = {}
        data = {
            **{
                "roles": [],
                "claims": {"shop": [], "organization": []},
                "iss": "issuer",
                "aud": "audition",
                "auth_time": "time",
                "user_id": user_id or "1234",
                "sub": "sub",
                "iat": 1595838390,
                "exp": 1595839390,
                "email": "email@test.com",
                "email_verified": False,
                "firebase": {
                    "identities": {"email": ["email@test.com"]},
                    "sign_in_provider": "custom",
                },
            },
            **overwrites,
        }
        if sysadmin:
            data["roles"].append("sysadmin")
        if admin:
            data["roles"].append("admin")
        if staff:
            data["roles"].append("staff")
        if shops:
            data["claims"]["shop"].extend(shops)
            data["roles"].append("staff")
        if organizations:
            data["claims"]["organization"].extend(organizations)
            data["roles"].append("admin")
        return jwt.encode(data, "secret-key")

    return generate


@pytest.fixture
def empty_token():
    return jwt.encode({}, "secret-key")


@pytest.fixture
def csv_blob_from_gcs():
    return "header1,header2\nrow1-1,row1-2".encode("utf-8")


@pytest.fixture
def mock_db():
    """Mock firestore Client"""
    yield firestore.CLIENT


@pytest.fixture
def with_firestore_docs(mock_db):
    def generate(path, doc_count=1, id_prefix="test_document"):
        output = []
        for i in range(doc_count):
            doc_dict = {
                "number": i+1,
                "string": f"string{i}",
                "bool": i % 2 == 0,
                "nest_dict": {
                    "number": i+1,
                    "string": f"string{i}",
                    "bool": i % 2 == 0,
                },
                "list": [i, i + 1, i + 2],
            }
            output.append(doc_dict)
            mock_db.document(f"{path}/{id_prefix}{i}").set(doc_dict)
        return output

    return generate
