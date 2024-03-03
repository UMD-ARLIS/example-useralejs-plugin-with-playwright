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

So long as your UserALE plugin is built and you have the `.env` file set up, you can run the following command to start the Playwright script with the UserALE plugin:

```bash
make run
```

Note: The first time you run the script, it will install the playwright headless browsers if you haven't already installed them.
