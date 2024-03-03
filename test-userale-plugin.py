#! /home/evan/mambaforge/envs/queststudio-cms/bin/python

import asyncio
import base64
import json
import logging
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Playwright


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

# Load plugin credentials from environment
USER_ID = os.getenv("USERALE_USER_ID")
PASSWORD = os.getenv("USERALE_PASSWORD")
URL = os.getenv("USERALE_ENDPOINT")

# constants
TIMEOUT_MS = int(os.getenv("TIMEOUT_MS", 5000))
CLOSEOUT_MS = int(os.getenv("CLOSEOUT_MS", 15000))
PATH_TO_EXTENSION = os.getenv("PATH_TO_EXTENSION", None)
USER_DATA_DIR = os.getenv("USER_DATA_DIR", None)

# Validation
if PATH_TO_EXTENSION is None:
    raise ValueError("PATH_TO_EXTENSION must be set in the environment")
if USER_DATA_DIR is None:
    raise ValueError("USER_DATA_DIR must be set in the environment")


def build_config(
    url,
    user_id,
    password,
    tool_name="useralePlugin",
    version="2.4.0",
    url_whitelist="github.com",
):
    # Encrypt the authHeader with base64 for basic auth
    auth_header = f'Basic {base64.b64encode(f"{user_id}:{password}".encode("utf-8")).decode("utf-8")}'

    # Construct useraleConfig object
    userale_config = {
        "url": url,
        "userId": user_id,
        "authHeader": auth_header,
        "toolName": tool_name,
        "version": version,
    }

    # Construct pluginConfig object
    plugin_config = {"urlWhitelist": url_whitelist}

    # Construct the overall configuration object
    config = {"useraleConfig": userale_config, "pluginConfig": plugin_config}

    return json.dumps(config)


async def run(p: Playwright):
    context = await p.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False,
        args=[
            f"--disable-extensions-except={PATH_TO_EXTENSION}",
            f"--load-extension={PATH_TO_EXTENSION}",
        ],
    )

    if len(context.background_pages) == 0:
        background_page = await context.wait_for_event("backgroundpage")
    else:
        background_page = context.background_pages[0]

    config_string = build_config(
        url=URL,
        user_id=USER_ID,
        password=PASSWORD,
        url_whitelist="github.com",
    )
    await background_page.evaluate(
        f"""
        window.updateConfig({config_string});
        window.config;
        """
    )

    #
    # Run Playwright workflow / test as your normally would
    # e.g.:
    #

    # Create a new page in the browser context
    logger.info("Starting playwright")
    page = await context.new_page()

    # Navigate to a page
    logger.info("Navigating to test page")
    await page.goto("https://github.com/")
    await page.wait_for_timeout(TIMEOUT_MS)

    # Click my user icon
    element = await page.query_selector('a[href="/pricing"]')
    await element.click()
    await page.wait_for_timeout(TIMEOUT_MS)

    # Sleep for a bit to allow the plugin to capture the events
    await page.wait_for_timeout(CLOSEOUT_MS)
    await context.close()


async def main():
    async with async_playwright() as p:
        await run(p)


asyncio.run(main())
