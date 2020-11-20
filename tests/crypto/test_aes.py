
from styler_rest_framework.crypto import aes
import pytest


class TestEncrypt:
    """ Tests for encrypt method
    """
    def test_no_key(self):
        with pytest.raises(ValueError) as expected:
            _ = aes.encrypt(None, 'something')

        assert str(expected.value) == 'Key is missing'

    def test_no_data(self):
        with pytest.raises(ValueError) as expected:
            _ = aes.encrypt('key', None)

        assert str(expected.value) == 'Data is missing'

    def test_encrypt_data(self):
        result = aes.encrypt('a long key', 'some data')

        decrypt = aes.decrypt('a long key', result)

        assert decrypt == 'some data'


class TestDecrypt:
    """ Tests for decrypt method
    """
    def test_no_key(self):
        with pytest.raises(ValueError) as expected:
            _ = aes.decrypt(None, 'data')

        assert str(expected.value) == 'Key is missing'

    def test_no_data(self):
        with pytest.raises(ValueError) as expected:
            _ = aes.decrypt('key', None)

        assert str(expected.value) == 'Data is missing'

    def test_decrypt_data(self):
        result = aes.encrypt('a long key', 'some data')
        result = '1234' + result[4:]

        with pytest.raises(aes.DecryptError):
            _ = aes.decrypt('a long key', result)

    def test_decrypt_modified_data(self):
        result = aes.encrypt('a long key', 'some data')

        decrypt = aes.decrypt('a long key', result)

        assert decrypt == 'some data'
