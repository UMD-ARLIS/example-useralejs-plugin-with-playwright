import logging
from typing import Optional
from playwright.async_api import Playwright
from src.lib.plugin import create_plugin_context
from src.lib.utils import run_or_loop
from src.lib.workflow import Workflow
from src.types import RunMode


async def run(
    p: Playwright, workflow: Workflow, mode: RunMode, logger: logging.Logger, **kwargs
):
    # Build playwright BrowserContext with UserALE plugin
    context = await create_plugin_context(playwright=p, **kwargs)

    # Create a new page in the browser context
    logger.info("Starting playwright")
    page = await context.new_page()

    # Instantiate workflow class
    wf = workflow(page=page)

    logger.info(f"Starting {mode} for {wf}")
    await run_or_loop(workflow, mode)

    await context.close()
