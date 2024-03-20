import pytest
from bot.lib.utils import run_or_loop
from bot.lib.workflow import Workflow


class TestRunOrLoop:
    @pytest.fixture
    def workflow_mock(self, mocker):
        return mocker.MagicMock(spec=Workflow)

    @pytest.mark.asyncio
    async def test_run_mode_calls_run_method(self, workflow_mock):
        # Arrange
        mode = "run"

        # Act
        await run_or_loop(workflow_mock, mode)

        # Assert
        workflow_mock.run.assert_called_once()
        workflow_mock.loop.assert_not_called()

    @pytest.mark.asyncio
    async def test_loop_mode_calls_loop_method(self, workflow_mock):
        # Arrange
        mode = "loop"

        # Act
        await run_or_loop(workflow_mock, mode)

        # Assert
        workflow_mock.loop.assert_called_once()
        workflow_mock.run.assert_not_called()

    @pytest.mark.asyncio
    async def test_invalid_mode_raises_value_error(self, workflow_mock):
        # Arrange
        mode = "invalid_mode"

        # Act & Assert
        with pytest.raises(ValueError):
            await run_or_loop(workflow_mock, mode)
