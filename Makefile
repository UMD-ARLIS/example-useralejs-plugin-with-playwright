.PHONY: poetry-config install-deps install-browsers run test list-workflows

# Target to configure poetry to use a local virtual environment
poetry-config:
	poetry config virtualenvs.in-project true

# Target to install dependencies into the virtual environment
install-deps: poetry-config
	poetry install

# Target to install browsers for Playwright
install-browsers:
	poetry run playwright install

# Target to run the Playwright script
run: install-deps install-browsers
	poetry run python main.py $(workflow_type) $(mode)

# Target to run tests using pytest
test: install-deps
	poetry run pytest

# Target to list available workflows
list-workflows: install-deps
	poetry run python -c "from bot.workflows.utils import list_workflows; list_workflows()"