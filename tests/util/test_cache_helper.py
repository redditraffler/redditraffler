import pytest
from pytest_mock import MockerFixture

from app.util import cache_helper


@pytest.fixture
def cache_mock(mocker: MockerFixture):
    return mocker.patch("app.util.cache_helper.cache")


class TestFetch:
    def test_cache_hit(self, mocker: MockerFixture, cache_mock):
        cache_mock.get = mocker.Mock(return_value="someValue")

        result = cache_helper.fetch("someKey")

        assert result == "someValue"

    def test_cache_miss_no_generator(self, mocker: MockerFixture, cache_mock):
        cache_mock.get = mocker.Mock(return_value=None)
        cache_mock.set = mocker.Mock()

        result = cache_helper.fetch("someKey2")

        assert result is None
        cache_mock.set.assert_not_called()

    def test_cache_miss_with_generator(self, mocker: MockerFixture, cache_mock):
        cache_mock.get = mocker.Mock(return_value=None)
        cache_mock.set = mocker.Mock(return_value=True)

        some_expensive_fn = mocker.Mock(return_value={"some": "info"})
        result = cache_helper.fetch(
            "someKeyWithGen", value_generator=some_expensive_fn, ttl_seconds=60
        )

        some_expensive_fn.assert_called_once()
        cache_mock.set.assert_called_with("someKeyWithGen", result, timeout=60)
        assert result == {"some": "info"}

    def test_cache_miss_with_generator_failed_set(
        self, mocker: MockerFixture, cache_mock
    ):
        cache_mock.get = mocker.Mock(return_value=None)
        cache_mock.set = mocker.Mock(return_value=False)

        some_expensive_fn = mocker.Mock(return_value=5)

        with pytest.raises(RuntimeError):
            cache_helper.fetch(
                "someKeyWithGenFailedSet",
                value_generator=some_expensive_fn,
                ttl_seconds=60,
            )

