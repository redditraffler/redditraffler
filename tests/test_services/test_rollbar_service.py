from app.services import rollbar
import pytest
import flask

TEST_TOKEN = "test_token"
TEST_CALLER_NAME = "some_caller_name"


@pytest.fixture
def mock_test_app(mocker):
    app = mocker.Mock()
    app.config = {
        "ENV": "test",
        "ROLLBAR_ACCESS_TOKEN": TEST_TOKEN,
        "ROLLBAR_ENABLED": False,
    }
    yield app


@pytest.fixture
def mock_prod_app(mocker):
    app = mocker.Mock()
    app.config = {
        "ENV": "production",
        "ROLLBAR_ACCESS_TOKEN": TEST_TOKEN,
        "ROLLBAR_ENABLED": True,
    }
    yield app


@pytest.fixture
def mock_get_caller_name(mocker):
    mock = mocker.patch("app.services.rollbar_service.get_caller_name")
    mock.return_value = TEST_CALLER_NAME
    yield mock


@pytest.fixture
def mock_report_message(mocker):
    yield mocker.patch("app.services.rollbar_service.rollbar.report_message")


class TestRollbarService:
    class TestInitApp:
        def test_init_with_disabled_flag(self, mocker, mock_test_app):
            rollbar_sdk_init = mocker.patch("app.services.rollbar_service.rollbar.init")
            rollbar.init_app(mock_test_app)
            rollbar_sdk_init.assert_called_with(
                TEST_TOKEN, "test", enabled=False, allow_logging_basic_config=False
            )

        def test_init_with_enabled_flag(self, mocker, mock_prod_app):
            rollbar_sdk_init = mocker.patch("app.services.rollbar_service.rollbar.init")
            rollbar.init_app(mock_prod_app)
            rollbar_sdk_init.assert_called_with(
                TEST_TOKEN, "production", enabled=True, allow_logging_basic_config=False
            )

    class TestException:
        def test_exception_call(self, mocker, mock_get_caller_name):
            request_mock = mocker.patch("app.services.rollbar_service.request")
            rollbar_report_exc_info = mocker.patch(
                "app.services.rollbar_service.rollbar.report_exc_info"
            )
            rollbar.exception()
            rollbar_report_exc_info.assert_called_with(
                extra_data={"context": {"source": TEST_CALLER_NAME}},
                level="error",
                request=request_mock,
            )

    class TestCritical:
        def test_critical_call(self, mocker, mock_get_caller_name, mock_report_message):
            request_mock = mocker.patch("app.services.rollbar_service.request")
            rollbar.critical("A critical log")
            mock_report_message.assert_called_with(
                f"[{TEST_CALLER_NAME}] A critical log",
                extra_data={"context": {}},
                level="critical",
                request=request_mock,
            )

    class TestError:
        def test_error_call(self, mocker, mock_get_caller_name, mock_report_message):
            request_mock = mocker.patch("app.services.rollbar_service.request")
            rollbar.error("An error log")
            mock_report_message.assert_called_with(
                f"[{TEST_CALLER_NAME}] An error log",
                extra_data={"context": {}},
                level="error",
                request=request_mock,
            )

    class TestWarn:
        def test_warn_call(self, mocker, mock_get_caller_name, mock_report_message):
            request_mock = mocker.patch("app.services.rollbar_service.request")
            rollbar.warn("A warn log", {"some": "context"})
            mock_report_message.assert_called_with(
                f"[{TEST_CALLER_NAME}] A warn log",
                extra_data={"context": {"some": "context"}},
                level="warning",
                request=request_mock,
            )

    class TestInfo:
        def test_info_call(self, mocker, mock_get_caller_name, mock_report_message):
            request_mock = mocker.patch("app.services.rollbar_service.request")
            rollbar.info("An info log")
            mock_report_message.assert_called_with(
                f"[{TEST_CALLER_NAME}] An info log",
                extra_data={"context": {}},
                level="info",
                request=request_mock,
            )

    class TestDebug:
        def test_debug_call(self, mocker, mock_get_caller_name, mock_report_message):
            request_mock = mocker.patch("app.services.rollbar_service.request")
            rollbar.debug("A debug log")
            mock_report_message.assert_called_with(
                f"[{TEST_CALLER_NAME}] A debug log",
                extra_data={"context": {}},
                level="debug",
                request=request_mock,
            )
