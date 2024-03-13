from src.lib.workflow import Workflow
from src.types import RunMode


async def run_or_loop(workflow: Workflow, mode: RunMode):
    """Run the workflow in the specified mode."""
    method_to_call = getattr(workflow, mode, None)
    if method_to_call:
        await method_to_call()
    else:
        raise ValueError("Invalid mode. Please specify 'run' or 'loop'.")
