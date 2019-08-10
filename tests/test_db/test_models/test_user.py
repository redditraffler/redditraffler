from app.db.models import User

import pytest


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
