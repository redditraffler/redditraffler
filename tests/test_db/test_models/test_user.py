from app.db.models import user as user_module

import jwt as pyjwt
import pytest


@pytest.fixture
def app_with_keys(app):
    app.config["ENC_KEY"] = b"oAG2nvtnITkBD1UJulsNUm52mMLyJ5FscwiUspxvUdM="
    app.config["SECRET_KEY"] = "haha what"
    yield app


@pytest.fixture
def user_with_refresh_token(user):
    user.refresh_token_enc = b"gAAAAABdRiRyp-uNXyEWQDtq7pYFEzl5ivTngPhqr3fz\
        NhEpES8CrsEnv_YvocLuMsQ8eQsUIUhQcRnoIsLmW3IFJGR9G9YgogZRiQo7rpx\
        Ls3nc3BBBj6I="  # Hello world decoder!
    yield user


def get_users_count(session):
    return session.query(user_module.User).count()


class TestUser:
    class TestFindByJwt:
        def test_returns_user_for_valid_jwt(self, app_with_keys, db_session):
            test_user = user_module.User(id=145, username="test")
            db_session.add(test_user)
            db_session.commit()

            jwt = pyjwt.encode(
                {"user_id": 145},
                key=app_with_keys.config["SECRET_KEY"],
                algorithm="HS256",
            )
            assert user_module.User.find_by_jwt(jwt) == test_user

        def test_returns_nil_when_user_not_found(self, app_with_keys, db_session):
            jwt = pyjwt.encode(
                {"user_id": 529},
                key=app_with_keys.config["SECRET_KEY"],
                algorithm="HS256",
            )
            assert user_module.User.find_by_jwt(jwt) is None

    class TestFindOrCreate:
        def test_minimum_username_length(self):
            with pytest.raises(ValueError):
                user_module.User.find_or_create("a")

        def test_returns_existing_user(self, user, db_session):
            old_user_count = get_users_count(db_session)
            user = user_module.User.find_or_create("test_user")
            new_user_count = get_users_count(db_session)

            assert user.username == "test_user"
            assert old_user_count == new_user_count

        def test_creates_new_user(self, db_session):
            old_user_count = get_users_count(db_session)
            user = user_module.User.find_or_create("hey_i_am_a_new_test_user")
            new_user_count = get_users_count(db_session)

            assert user.username == "hey_i_am_a_new_test_user"
            assert user.id is not None
            assert new_user_count == old_user_count + 1

    class TestSetRefreshToken:
        def test_requires_nonempty_refresh_token(self, user, app_with_keys):
            with pytest.raises(ValueError):
                user.set_refresh_token("")

        def test_encrypts_token_and_saves(self, user, app_with_keys, db_session):
            assert user.refresh_token_enc is None
            user.set_refresh_token("hey_this_is_some_refresh_token")
            saved_token = db_session.query(user_module.User).first().refresh_token_enc
            assert saved_token is not None
            assert type(saved_token) == bytes

    class TestGetRefreshToken:
        def test_user_must_have_token(self, user, app_with_keys):
            with pytest.raises(AttributeError):
                user.get_refresh_token()

        def test_retrieves_plaintext_refresh_token(
            self, user_with_refresh_token, app_with_keys
        ):
            refresh_token_str = user_with_refresh_token.get_refresh_token()
            assert refresh_token_str == "hello world decoder!"

    class TestGetJwt:
        def test_encodes_user_info(self, user, app_with_keys):
            jwt = user.get_jwt()
            assert pyjwt.decode(jwt, key="haha what", algorithms=["HS256"]) == {
                "user_id": user.id,
                "username": user.username,
            }

