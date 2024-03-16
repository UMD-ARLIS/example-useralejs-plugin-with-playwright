import pytest
from main import parse_args


class TestParseArgs:
    def test_parse_args_valid_input(self, monkeypatch):
        # Mocking command line arguments
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "github-anomalous",
                "--mode",
                "run",
                "--kwargs",
                '{"key": "value"}',
            ],
        )
        args = parse_args()
        assert args.workflow_type == "github-anomalous"
        assert args.mode == "run"
        assert args.kwargs == {"key": "value"}

    def test_parse_args_missing_mode(self, monkeypatch):
        # Mocking command line arguments
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "github-normal",
                "--kwargs",
                '{"key": "value"}',
            ],
        )
        args = parse_args()
        assert args.mode == "run"

    def test_parse_args_invalid_workflow_type(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "invalid_workflow",
                "--mode",
                "run",
                "--kwargs",
                '{"key": "value"}',
            ],
        )
        # Testing invalid workflow type
        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_invalid_mode(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "github-anomalous",
                "--mode",
                "invalid_mode",
                "--kwargs",
                '{"key": "value"}',
            ],
        )
        # Testing invalid mode
        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_invalid_kwargs(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "github-anomalous",
                "--mode",
                "run",
                "--kwargs",
                "invalid_json",
            ],
        )
        # Testing invalid kwargs (not a valid JSON string)
        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_no_args(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["main.py"])
        # Testing no arguments provided
        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_invalid_number_of_args(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "github-anomalous",
                "--mode",
                "run",
                "--kwargs",
                '{"key": "value"}',
                "extra_arg",
            ],
        )
        # Testing invalid number of arguments
        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_empty_kwargs(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "github-anomalous",
                "--mode",
                "run",
                "--kwargs",
                "{}",
            ],
        )
        # Testing empty kwargs
        args = parse_args()
        assert args.kwargs == {}

    def test_parse_args_multiple_keyword_arguments(self, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            [
                "main.py",
                "--workflow_type",
                "github-normal",
                "--mode",
                "run",
                "--kwargs",
                '{"key1": "value1", "key2": "value2"}',
            ],
        )
        # Testing multiple keyword arguments
        args = parse_args()
        assert args.kwargs == {"key1": "value1", "key2": "value2"}
