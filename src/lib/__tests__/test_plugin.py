import base64
import json
import pytest
from src.lib.plugin import build_config


@pytest.mark.parametrize(
    "url, user_id, password, tool_name, version, url_whitelist, expected",
    [
        # Test case 1: All parameters provided
        (
            "https://example.com",
            "user123",
            "password123",
            "myTool",
            "1.0.0",
            "example\\.com/.*",
            {
                "useraleConfig": {
                    "url": "https://example.com",
                    "userId": "user123",
                    "toolName": "myTool",
                    "version": "1.0.0",
                    "authHeader": f'Basic {base64.b64encode("user123:password123".encode("utf-8")).decode("utf-8")}',
                },
                "pluginConfig": {"urlWhitelist": "example\\.com/.*"},
            },
        ),
        # Test case 2: Minimum parameters provided
        (
            "https://example.com",
            "user123",
            None,
            "useralePlugin",
            "2.4.0",
            ".*",
            {
                "useraleConfig": {
                    "url": "https://example.com",
                    "userId": "user123",
                    "toolName": "useralePlugin",
                    "version": "2.4.0",
                },
                "pluginConfig": {"urlWhitelist": ".*"},
            },
        ),
        # Test case 3: Password is provided
        (
            "https://example.com",
            "user123",
            "password123",
            "useralePlugin",
            "2.4.0",
            ".*",
            {
                "useraleConfig": {
                    "url": "https://example.com",
                    "userId": "user123",
                    "toolName": "useralePlugin",
                    "version": "2.4.0",
                    "authHeader": f'Basic {base64.b64encode("user123:password123".encode("utf-8")).decode("utf-8")}',
                },
                "pluginConfig": {"urlWhitelist": ".*"},
            },
        ),
        # Add more test cases for other permutations as needed
    ],
)
def test_build_config(
    url, user_id, password, tool_name, version, url_whitelist, expected
):
    assert build_config(
        url, user_id, password, tool_name, version, url_whitelist
    ) == json.dumps(expected)
