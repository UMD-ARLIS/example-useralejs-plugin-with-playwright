# UserALE Plugin

This repository provides an example of how to use the [Apache Flagon UserALE](https://github.com/apache/flagon-useralejs) Browser plugin while using Playwright. It assumes you already have built the plugin and have it somewhere on your local machine.

Note: Browser plugins _only_ work with the chromium browser in Playwright. 

## Setup

### 0. Prerequisites

- [Node.js](https://nodejs.org/en/download/)
- [Python 3](https://www.python.org/downloads/)
- Build the UserALE plugin:
    1. Clone [UserALE](https://github.com/apache/flagon-useralejs)
    2. Fetch the latest version of the plugin and build it:
    ```bash
    git fetch origin test
    git switch test
    npm i && npm run build
    ```
    3. Find the plugin located at the `build/UserALEWebExtension` directory which will be created

### 1. Environment Setup

1. Copy the `.env.example` file and rename it to `.env`.
2. Fill in the required environment variables in the `.env` file:
   - `USERALE_USER_ID`: The user ID used for authentication with the UserALE service.
   - `USERALE_PASSWORD`: The password used for authentication with the UserALE service.
   - `USERALE_ENDPOINT`: The endpoint where UserALE logs are sent.

### 2. Virtual Environment Setup

Make sure you have Python 3 installed on your system.

1. Create a virtual environment by running the following command in your terminal:
```bash
make venv
```

2. Install the dependencies:
```bash
make install-deps
```

### 3. Run playwright with the UserALE plugin

For anomalous data generation, we have two workflows:

## Bot Data Generation Workflows

This document outlines two distinct workflows for generating data logs. Each workflow consists of a series of steps executed with specific conditions.

### Workflow 1: Anomalous Data Logs
_This workflow does not have any wait time between steps._

1. Toggle Chrome extensions plugin **"User ALE Extension"** on.
2. Navigate to [PyTorch GitHub Repository](https://github.com/pytorch/pytorch).
3. Click through the following navigation sequence: `folder "torch"` → `folder "cuda"` → `file "basic.py"`.
4. Collapse a method by clicking the dropdown icon to the right of line 122.
5. Open the method back up by clicking the same dropdown.
6. Click back into the `pytorch/pytorch` directory at the top of the page.
7. Toggle Chrome extensions plugin **"User ALE Extension"** off.

### Workflow 2: Normal Data Logs
_This workflow includes a 2-second wait time between every step._

1. Toggle Chrome extensions plugin **"User ALE Extension"** on.
2. Navigate to [PyTorch GitHub Repository](https://github.com/pytorch/pytorch).
3. Click through the following navigation sequence: `folder "torch"` → `folder "cuda"` → `file "basic.py"`.
4. Scroll down to line 122.
5. Collapse a method by clicking the dropdown icon to the right of line 122.
6. Open the method back up by clicking the same dropdown.
7. Scroll back up to the top of the page.
8. Click back into the `pytorch/pytorch` directory at the top of the page.
9. Toggle Chrome extensions plugin **"User ALE Extension"** off.

At the moment, the command to run this bot will follow "normal" log data generation. Although, if we'd like to generate anomalous logs of data, this can be done by simply setting the second parameter of the `await run()` call to "anomalous", rather than "normal"

## Running the Bot

So long as your UserALE plugin is built and you have the `.env` file set up, you can run the following command to start the Playwright script with the UserALE plugin.

```bash
make run
```

Note: The first time you run the script, it will install the playwright headless browsers if you haven't already installed them.
