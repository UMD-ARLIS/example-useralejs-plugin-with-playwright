import logging

import pytest
from bot.lib.run import run
from bot.lib.workflow import Workflow
from playwright.async_api import Playwright


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
    @pytest.mark.parametrize("use_plugin", [True, False])
    async def test_run_function(
        self, mocker, p_mock, workflow_mock, logger_mock, use_plugin
    ):
        # Patch async functions
        context_mock = mocker.patch(
            (
                "bot.lib.run.create_plugin_context"
                if use_plugin
                else "bot.lib.run.create_default_context"
            ),
            return_value=mocker.AsyncMock(),
        )

        run_or_loop_mock = mocker.patch(
            "bot.lib.run.run_or_loop", return_value=mocker.AsyncMock()
        )

        # Set up expectations for mock objects
        expected_mode = "run"
        expected_kwargs = {"key": "value"}

        # Run the function with mocked dependencies
        await run(
            p=p_mock,
            workflow=workflow_mock,
            mode=expected_mode,
            use_plugin=use_plugin,
            logger=logger_mock,
            **expected_kwargs,
        )

        # Assert that other calls we do not want to test were not called
        context_mock.assert_called_once()
        workflow_mock.assert_called_once()
        run_or_loop_mock.assert_called_once()
        assert logger_mock.info.call_count == 2
