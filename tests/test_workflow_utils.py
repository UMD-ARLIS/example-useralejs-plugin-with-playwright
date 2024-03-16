import pytest
from src.workflows.utils import import_workflow


class TestGetWorkflow:
    @pytest.mark.parametrize(
        "workflow_type, expected_class_name",
        [
            ("github-anomalous", "GithubAnomalousWorkflow"),
            ("github-normal", "GithubNormalWorkflow"),
            # Add more workflow types and their expected class names as needed
        ],
    )
    def test_get_workflow_returns_correct_class(
        self,
        workflow_type,
        expected_class_name,
    ):
        # Act
        workflow = import_workflow(workflow_type)

        # Assert
        assert workflow.__name__ == expected_class_name

    def test_get_workflow_raises_key_error_for_invalid_workflow_type(self):
        # Arrange
        invalid_workflow_type = "invalid_workflow_type"

        # Act & Assert
        with pytest.raises(KeyError):
            import_workflow(invalid_workflow_type)
