import pytest
import logging

from app.logging import (
    _get_log_level_from_config,
    _configure_main_logger,
    _configure_rollbar,
)


class TestGetLogLevelFromConfig:
    @pytest.fixture
    def invalid_cfg_app(self, mocker):
        app = mocker.Mock()
        app.config = {"LOG_LEVEL": "SOME_INVALID_LEVEL"}
        yield app

    @pytest.fixture
    def valid_cfg_app(self, mocker):
        app = mocker.Mock()
        app.config = {"LOG_LEVEL": "NOTSET"}
        yield app

    def test_default_to_info(self, invalid_cfg_app):
        result = _get_log_level_from_config(invalid_cfg_app)
        assert result == logging.INFO

    def test_assigns_valid_log_level_from_cfg(self, valid_cfg_app):
        result = _get_log_level_from_config(valid_cfg_app)
        assert result == logging.NOTSET


class TestConfigureMainLogger:
    TEST_LOG_LEVEL = logging.DEBUG

    @pytest.fixture
    def app_with_logger(self, mocker):
        app = mocker.Mock()
        app.logger.setLevel = mocker.Mock()
        yield app

    def test_set_expected_log_level(self, app_with_logger):
        _configure_main_logger(app_with_logger, TestConfigureMainLogger.TEST_LOG_LEVEL)
        app_with_logger.logger.setLevel.assert_called_with(
            TestConfigureMainLogger.TEST_LOG_LEVEL
        )


class TestConfigureRollbar:
    TEST_LOG_LEVEL = logging.CRITICAL

    @pytest.fixture
    def valid_cfg_app(self, mocker):
        app = mocker.Mock()
        app.config = {
            "ENV": "SomeEnvironment",
            "ROLLBAR_ENABLED": False,
            "ROLLBAR_ACCESS_TOKEN": "SomeApiToken",
        }
        app.logger.addHandler = mocker.Mock()
        yield app

    @pytest.fixture
    def invalid_cfg_app(self, mocker):
        app = mocker.Mock()
        app.config = {}
        yield app

    def test_successful_config(self, valid_cfg_app, mocker):
        rollbar_mock = mocker.patch("app.logging.rollbar")
        rollbar_mock.init = mocker.Mock()
        rollbar_handler_mock = mocker.patch("app.logging.RollbarHandler")
        rollbar_handler_mock.return_value.setLevel = mocker.Mock()

        _configure_rollbar(valid_cfg_app, TestConfigureRollbar.TEST_LOG_LEVEL)
        rollbar_mock.init.assert_called_with(
            "SomeApiToken",
            "SomeEnvironment",
            handler="blocking",
            enabled=False,
            allow_logging_basic_config=False,
        )
        rollbar_handler_mock.assert_called_with(history_size=5)
        rollbar_handler_mock.return_value.setLevel.assert_called_with(
            TestConfigureRollbar.TEST_LOG_LEVEL
        )
        valid_cfg_app.logger.addHandler.assert_called_with(
            rollbar_handler_mock.return_value
        )

    def test_missing_config(self, invalid_cfg_app):
        with pytest.raises(KeyError):
            _configure_rollbar(invalid_cfg_app, TestConfigureRollbar.TEST_LOG_LEVEL)
