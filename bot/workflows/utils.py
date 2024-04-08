from importlib import import_module
from typing import Dict
from typing import Tuple

import colorama
from bot.lib.types import WorkflowType
from bot.lib.workflow import Workflow
from colorama import Fore

colorama.init(autoreset=True)

workflow_classes: Dict[WorkflowType, Tuple[str, str]] = {
    "github-anomalous": (
        "GithubAnomalousWorkflow",
        "Workflow in PyTorch GitHub repo with intentionally anomalous behavior.",
    ),
    "github-normal": (
        "GithubNormalWorkflow",
        "Workflow in PyTorch GitHub repo with normal behavior.",
    ),
    "superset-graph-experienced": (
        "SupersetGraphExperiencedWorkflow",
        "Workflow for creating a funnel diagram in Apache Superset with experienced user.",
    ),
    "superset-graph-inexperienced": (
        "SupersetGraphInexperiencedWorkflow",
        "Workflow for creating a funnel diagram in Apache Superset with inexperienced user.",
    ),
}


def import_workflow(workflow_type: WorkflowType) -> Workflow:
    """Return the workflow class for the specified workflow type."""
    workflow_module = import_module("bot.workflows")
    workflow_class_name, _ = workflow_classes[workflow_type]
    workflow_class = getattr(workflow_module, workflow_class_name)
    return workflow_class


def list_workflows(describe: bool = True) -> None:
    """List all available workflows."""
    if describe:
        print("Available workflows:")
        for workflow_type, (_, description) in workflow_classes.items():
            print(f"- {Fore.CYAN}{workflow_type}{Fore.RESET}: {description}")
    else:
        print("Available workflows:")
        for workflow_type in workflow_classes:
            print(f"- {Fore.CYAN}{workflow_type}{Fore.RESET}")
