import logging
from playwright.async_api import Playwright
import pytest

from src.lib.workflow import Workflow
from src.run import run


class TestRun:
    @pytest.fixture
    def p_mock(self, mocker):
        return mocker.MagicMock(spec=Playwright)

    @pytest.fixture
    def workflow_mock(self, mocker):
        return mocker.MagicMock(spec=Workflow)

    @pytest.fixture
    def logger_mock(self, mocker):
        return mocker.MagicMock(spec=logging.Logger)

    @pytest.mark.asyncio
    async def test_run_function(self, mocker, p_mock, workflow_mock, logger_mock):
        # Patch async functions
        create_plugin_context_mock = mocker.patch(
            "src.run.create_plugin_context",
            return_value=mocker.AsyncMock(),
        )
        run_or_loop_mock = mocker.patch(
            "src.run.run_or_loop", return_value=mocker.AsyncMock()
        )

        # Set up expectations for mock objects
        expected_mode = "run"
        expected_kwargs = {"key": "value"}

        # Run the function with mocked dependencies
        await run(p_mock, workflow_mock, expected_mode, logger_mock, **expected_kwargs)

        # Assert that other calls we do not want to test were not called
        workflow_mock.assert_called_once()
        create_plugin_context_mock.assert_called_once()
        run_or_loop_mock.assert_called_once()
        assert logger_mock.info.call_count == 2
