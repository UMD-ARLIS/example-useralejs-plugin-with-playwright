import base64
import json
from typing import Optional

from bot.config import cfg
from playwright.async_api import BrowserContext
from playwright.async_api import Playwright


def build_config(
    url: str,
    user_id: str,
    password: Optional[str] = None,
    tool_name: Optional[str] = "useralePlugin",
    version: Optional[str] = "2.4.0",
    url_whitelist: Optional[str] = ".*",
) -> str:
    """
    Build a UserALE plugin configuration object.

    Arguments:
        url -- the UserALE endpoint URL
        user_id -- the UserALE user ID
        password -- the UserALE password
        tool_name -- the name of the tool
        version -- the version of the tool
        url_whitelist -- a regular expression to whitelist URLs for logging

    Returns:
        str -- a JSON string representing the UserALE plugin configuration object
    """

    # Construct useraleConfig object
    userale_config = {
        "url": url,
        "userId": user_id,
        "toolName": tool_name,
        "version": version,
    }
    if password:
        # Encrypt the authHeader with base64 for basic auth
        auth_header = f'Basic {base64.b64encode(f"{user_id}:{password}".encode("utf-8")).decode("utf-8")}'
        userale_config.update({"authHeader": auth_header})

    # Construct pluginConfig object
    plugin_config = {"urlWhitelist": url_whitelist}

    # Construct the overall configuration object
    config = {"useraleConfig": userale_config, "pluginConfig": plugin_config}

    return json.dumps(config)


async def create_plugin_context(playwright: Playwright, **kwargs) -> BrowserContext:
    """
    Create a playwright browser context with the UserALE plugin installed.

    Arguments:
        playwright -- the playwright object
        kwargs -- additional configuration options for the plugin

    Returns:
        BrowserContext -- the playwright browser context with the plugin installed
    """
    # Fetch config values
    url = kwargs.pop("url", cfg.url)
    user_id = kwargs.pop("user_id", cfg.user_id)
    password = kwargs.pop("password", cfg.password)
    user_data_dir = (
        kwargs.pop("user_data_dir", cfg.user_data_dir)
        or f"/tmp/flagon-demo-bot-{user_id}"
    )
    headless: bool = kwargs.pop("headless", True)

    # Validate config values
    if not url:
        raise ValueError("Missing url for UserALE endpoint. Please set the URL in the configuration.")
    if not user_id:
        raise ValueError("Missing user_id for UserALE. Please set the user_id in the configuration.")

    context = await playwright.chromium.launch_persistent_context(
        user_data_dir,
        headless=headless,
        args=[
            f"--disable-extensions-except={cfg.path_to_extension}",
            f"--load-extension={cfg.path_to_extension}",
        ],
    )

    if len(context.background_pages) == 0:
        background_page = await context.wait_for_event("backgroundpage")
    else:
        background_page = context.background_pages[0]

    config_string = build_config(url=url, user_id=user_id, password=password, **kwargs)
    await background_page.evaluate(
        f"""
        browser.storage.local.set({config_string});
        window.updateConfig({config_string});
        window.config;
        """
    )
    return context
