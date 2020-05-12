import pytest

from app.commands import delete, clear_cache
from tests.factories import RaffleFactory


@pytest.fixture
def runner(app):
    yield app.test_cli_runner()


@pytest.fixture
def raffle():
    return RaffleFactory()


class TestDelete:
    class TestInvalidRaffleId:
        def test_graceful_failure(self, runner, db):
            TEST_BOGUS_RAFFLE_ID = "abc123"
            result = runner.invoke(delete, ["--raffle_id", TEST_BOGUS_RAFFLE_ID])
            assert f"Raffle '{TEST_BOGUS_RAFFLE_ID}' does not exist." in result.output

    class TestValidRaffleId:
        def test_deletes_raffle(self, runner, mocker, db_session, raffle):
            mocker.patch("app.commands.click.confirm")

            result = runner.invoke(delete, ["--raffle_id", raffle.submission_id])

            assert f"Successfully removed {raffle.submission_id}" in result.output
            raffle = db_session.execute(
                "SELECT * FROM raffle WHERE id = :id", {"id": raffle.id}
            ).first()
            assert not raffle

    class TestDeleteFailed:
        def test_rolled_back(self, runner, mocker, raffle):
            mocker.patch("app.commands.click.confirm")
            delete_mock = mocker.patch("app.commands.db.session.delete")
            delete_mock.side_effect = ValueError("some random error")
            rollback_mock = mocker.patch("app.commands.db.session.rollback")

            result = runner.invoke(delete, ["--raffle_id", raffle.submission_id])

            rollback_mock.assert_called_once()
            assert "Something went wrong while deleting the raffle" in result.output
            assert "some random error" in result.output


class TestClearCache:
    def test_call_clear_cache(self, runner, mocker):
        cache_mock = mocker.patch("app.commands.cache")
        cache_mock.clear = mocker.Mock()

        result = runner.invoke(clear_cache)

        cache_mock.clear.assert_called_once()
        assert "Cache cleared" in result.output
