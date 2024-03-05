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

load_dotenv(".env")

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


async def anomalous_bot(page):

    # Navigate to pytorch/pytorch/torch/cuda/__init__.py using first CSS selector matches
    await page.locator('a[title="torch"][aria-label="torch, (Directory)"]').nth(
        1
    ).click()
    await page.locator('a[title="cuda"][aria-label="cuda, (Directory)"]').nth(1).click()
    await page.locator('a[title="__init__.py"][aria-label="__init__.py, (File)"]').nth(
        1
    ).click()

    # Collapse and open is_bf16_supported() method
    await page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()
    await page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()

    # Navigate back to pytorch/pytorch
    await page.locator(
        'a[data-pjax="#repo-content-pjax-container"][data-turbo-frame="repo-content-turbo-frame"][href="/pytorch/pytorch"]'
    ).nth(1).click()


async def normal_bot(page):

    await asyncio.sleep(2)  # 2-second wait
    # Navigate to pytorch/pytorch/torch/cuda/__init__.py using first CSS selector matches
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 15)")
    await asyncio.sleep(2)
    await page.locator('a[title="torch"][aria-label="torch, (Directory)"]').nth(
        1
    ).click()
    await asyncio.sleep(2)
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
    await asyncio.sleep(2)
    await page.locator('a[title="cuda"][aria-label="cuda, (Directory)"]').nth(1).click()
    await asyncio.sleep(2)
    await page.locator('a[title="__init__.py"][aria-label="__init__.py, (File)"]').nth(
        1
    ).click()
    await asyncio.sleep(2)

    # Collapse and open is_bf16_supported() method
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 12)")
    await asyncio.sleep(2)
    await page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()
    await asyncio.sleep(2)
    await page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()
    await asyncio.sleep(2)
    await page.evaluate("window.scrollTo(0, 0)")
    await asyncio.sleep(2)

    # Navigate back to pytorch/pytorch
    await page.locator(
        'a[data-pjax="#repo-content-pjax-container"][data-turbo-frame="repo-content-turbo-frame"][href="/pytorch/pytorch"]'
    ).nth(1).click()
    await asyncio.sleep(2)


async def run(p: Playwright, type="normal"):
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
    config = await background_page.evaluate(
        f"""
        browser.storage.local.set({config_string});
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
    await page.goto("https://github.com/pytorch/pytorch")
    if type == "anomalous":
        await anomalous_bot(page)  # Add 'await' here
    else:
        await normal_bot(page)  # Ensure 'await' is used here too

    await context.close()


async def main():
    async with async_playwright() as p:
        await run(p, "anomalous")


asyncio.run(main())
