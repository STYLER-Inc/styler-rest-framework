""" Conftest
"""

import pytest
import jwt


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
                organizations=None
            ):
        if overwrites is None:
            overwrites = {}
        data = {**{
            'roles': [],
            'claims': {
                'shop': [],
                'organization': []
            },
            'iss': 'issuer',
            'aud': 'audition',
            'auth_time': 'time',
            'user_id': '1234',
            'sub': 'sub',
            'iat': 1595838390,
            'exp': 1595839390,
            'email': 'email@test.com',
            'email_verified': False,
            'firebase': {
                'identities': {
                    'email': ['email@test.com']
                },
                'sign_in_provider': 'custom'
            }
        }, **overwrites}
        if sysadmin:
            data['roles'].append('sysadmin')
        if admin:
            data['roles'].append('admin')
        if staff:
            data['roles'].append('staff')
        if shops:
            data['claims']['shop'].extend(shops)
            data['roles'].append('staff')
        if organizations:
            data['claims']['organization'].extend(organizations)
            data['roles'].append('admin')
        return jwt.encode(data, 'secret-key')
    return generate


@pytest.fixture
def empty_token():
    return jwt.encode({}, 'secret-key')
