import logging

from bot.lib.plugin import create_plugin_context
from bot.lib.types import RunMode
from bot.lib.utils import create_default_context
from bot.lib.utils import run_or_loop
from bot.lib.workflow import Workflow
from playwright.async_api import Playwright


async def run(
    p: Playwright,
    workflow: Workflow,
    mode: RunMode,
    use_plugin: bool,
    logger: logging.Logger,
    **kwargs,
):
    # Build playwright BrowserContext with UserALE plugin
    if use_plugin:
        context = await create_plugin_context(playwright=p, **kwargs)
    else:
        context = await create_default_context(playwright=p, **kwargs)

    # Create a new page in the browser context
    logger.info("Starting playwright")
    page = await context.new_page()

    # Instantiate workflow class
    wf = workflow(page=page)

    logger.info(f"Starting {mode} for {wf}")
    await run_or_loop(workflow=wf, mode=mode)

    await context.close()
