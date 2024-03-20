from playwright.async_api import Playwright
from src.lib.workflow import Workflow
from src.types import RunMode


async def run_or_loop(workflow: Workflow, mode: RunMode):
    """Run the workflow in the specified mode."""
    method_to_call = getattr(workflow, mode, None)
    if method_to_call:
        await method_to_call()
    else:
        raise ValueError("Invalid mode. Please specify 'run' or 'loop'.")


async def create_default_context(playwright: Playwright, **kwargs):
    """Create a default browser context."""
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="",
        headless=kwargs.get("headless", True),
    )
    return context
