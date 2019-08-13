from app.util import JwtHelper

import pytest
import jwt


TEST_SECRET_KEY = "lolwut"


@pytest.fixture(autouse=True)
def app_with_secret_key(app):
    app.config["SECRET_KEY"] = TEST_SECRET_KEY
    yield app


class TestJwtHelper:
    def test_encode(self):
        payload = {"a": 1, "b": 2}
        encoded_payload = JwtHelper.encode(payload)
        assert (
            jwt.decode(encoded_payload, TEST_SECRET_KEY, algorithms=["HS256"])
            == payload
        )

    def test_decode(self):
        encoded_payload = b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidGVzdCJ9.\
            YDNkA80OW1qGmzYjUU3Ie06F7VTiDWI0Ektw6R-92VE"
        decoded = jwt.decode(encoded_payload, TEST_SECRET_KEY, algorithms=["HS256"])
        assert decoded == {"user": "test"}
