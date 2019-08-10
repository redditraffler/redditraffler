from app.db.models import User

import pytest


@pytest.fixture
def app_with_enc_key(app):
    app.config["ENC_KEY"] = b"oAG2nvtnITkBD1UJulsNUm52mMLyJ5FscwiUspxvUdM="
    yield app


@pytest.fixture
def user_with_refresh_token(user):
    user.refresh_token_enc = b"gAAAAABdRiRyp-uNXyEWQDtq7pYFEzl5ivTngPhqr3fz\
        NhEpES8CrsEnv_YvocLuMsQ8eQsUIUhQcRnoIsLmW3IFJGR9G9YgogZRiQo7rpx\
        Ls3nc3BBBj6I="  # Hello world decoder!
    yield user


def get_users_count(session):
    return session.query(User).count()


class TestUser:
    class TestFindOrCreate:
        def test_minimum_username_length(self):
            with pytest.raises(ValueError):
                User.find_or_create("a")

        def test_returns_existing_user(self, user, db_session):
            old_user_count = get_users_count(db_session)
            user = User.find_or_create("test_user")
            new_user_count = get_users_count(db_session)

            assert user.username == "test_user"
            assert old_user_count == new_user_count

        def test_creates_new_user(self, db_session):
            old_user_count = get_users_count(db_session)
            user = User.find_or_create("hey_i_am_a_new_test_user")
            new_user_count = get_users_count(db_session)

            assert user.username == "hey_i_am_a_new_test_user"
            assert user.id is not None
            assert new_user_count == old_user_count + 1

    class TestSetRefreshToken:
        def test_requires_nonempty_refresh_token(self, user, app_with_enc_key):
            with pytest.raises(ValueError):
                user.set_refresh_token("")

        def test_encrypts_token_and_saves(self, user, app_with_enc_key, db_session):
            assert user.refresh_token_enc is None
            user.set_refresh_token("hey_this_is_some_refresh_token")
            saved_token = db_session.query(User).first().refresh_token_enc
            assert saved_token is not None
            assert type(saved_token) == bytes

    class TestGetRefreshToken:
        def test_user_must_have_token(self, user, app_with_enc_key):
            with pytest.raises(AttributeError):
                user.get_refresh_token()

        def test_retrieves_plaintext_refresh_token(
            self, user_with_refresh_token, app_with_enc_key
        ):
            refresh_token_str = user_with_refresh_token.get_refresh_token()
            assert refresh_token_str == "hello world decoder!"
