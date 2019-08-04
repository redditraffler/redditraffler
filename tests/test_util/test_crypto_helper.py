from app.util import CryptoHelper
from cryptography.fernet import Fernet

import pytest


TEST_KEY = b"oAG2nvtnITkBD1UJulsNUm52mMLyJ5FscwiUspxvUdM="


@pytest.fixture(autouse=True)
def app_with_fake_enc_key(app):
    app.config["ENC_KEY"] = TEST_KEY
    yield app


class TestCryptoHelper:
    class TestEncrypt:
        def test_encrypt_string(self):
            f = Fernet(TEST_KEY)
            test_str = "hello world!"
            test_str_enc_bytes = CryptoHelper.encrypt(test_str)
            assert f.decrypt(test_str_enc_bytes).decode() == test_str

        def test_encrypt_bytes_without_casting(self):
            f = Fernet(TEST_KEY)
            test_str_bytes = b"hey man"
            test_str_enc_bytes = CryptoHelper.encrypt(test_str_bytes)
            assert f.decrypt(test_str_enc_bytes).decode() == "hey man"

        def test_raises_when_input_is_not_bytes_or_string(self):
            with pytest.raises(ValueError):
                assert CryptoHelper.encrypt({})
            with pytest.raises(ValueError):
                assert CryptoHelper.encrypt([])
            with pytest.raises(ValueError):
                assert CryptoHelper.encrypt(None)

    class TestDecrypt:
        def test_encrypt_string_with_casting(self):
            test_str_enc = "gAAAAABdRiRyp-uNXyEWQDtq7pYFEzl5ivTngPhqr3fzNh\
                EpES8CrsEnv_YvocLuMsQ8eQsUIUhQcRnoIsLmW3IFJGR9G9YgogZRiQo7\
                rpxLs3nc3BBBj6I="  # "hello world decoder!" pre-converted
            test_str_bytes = CryptoHelper.decrypt(test_str_enc)
            assert test_str_bytes.decode() == "hello world decoder!"

        def test_decrypt_bytes(self):
            test_str_enc_bytes = b"gAAAAABdRiRyp-uNXyEWQDtq7pYFEzl5ivTngPhqr3fz\
                NhEpES8CrsEnv_YvocLuMsQ8eQsUIUhQcRnoIsLmW3IFJGR9G9YgogZRiQo7rpx\
                Ls3nc3BBBj6I="  # "hello world decoder!" pre-converted
            test_str_bytes = CryptoHelper.decrypt(test_str_enc_bytes)
            assert test_str_bytes.decode() == "hello world decoder!"

        def test_raises_when_input_is_not_bytes_or_string(self):
            with pytest.raises(ValueError):
                assert CryptoHelper.decrypt({})
            with pytest.raises(ValueError):
                assert CryptoHelper.decrypt([])
            with pytest.raises(ValueError):
                assert CryptoHelper.decrypt(None)
