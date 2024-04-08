import asyncio

from bot.lib.workflow import Workflow


class GithubAnomalousWorkflow(Workflow):
    async def run(self):
        await self.page.goto("https://github.com/pytorch/pytorch")

        # Navigate to pytorch/pytorch/torch/cuda/__init__.py using first CSS selector matches
        await self.page.locator(
            'a[title="torch"][aria-label="torch, (Directory)"]'
        ).nth(1).click()
        await self.page.locator('a[title="cuda"][aria-label="cuda, (Directory)"]').nth(
            1
        ).click()
        await self.page.locator(
            'a[title="__init__.py"][aria-label="__init__.py, (File)"]'
        ).nth(1).click()

        # Collapse and open is_bf16_supported() method
        await self.page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()
        await self.page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()

        # Navigate back to pytorch/pytorch
        await self.page.locator(
            'a[data-pjax="#repo-content-pjax-container"][data-turbo-frame="repo-content-turbo-frame"][href="/pytorch/pytorch"]'
        ).nth(1).click()

    def __str__(self):
        return "GithubAnomalousWorkflow"

    def __repr__(self):
        return "GithubAnomalousWorkflow()"


class GithubNormalWorkflow(Workflow):
    async def run(self):
        await self.page.goto("https://github.com/pytorch/pytorch")

        await asyncio.sleep(2)  # 2-second wait
        # Navigate to pytorch/pytorch/torch/cuda/__init__.py using first CSS selector matches
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 15)")
        await asyncio.sleep(2)
        await self.page.locator(
            'a[title="torch"][aria-label="torch, (Directory)"]'
        ).nth(1).click()
        await asyncio.sleep(2)
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
        await asyncio.sleep(2)
        await self.page.locator('a[title="cuda"][aria-label="cuda, (Directory)"]').nth(
            1
        ).click()
        await asyncio.sleep(2)
        await self.page.locator(
            'a[title="__init__.py"][aria-label="__init__.py, (File)"]'
        ).nth(1).click()
        await asyncio.sleep(2)

        # Collapse and open is_bf16_supported() method
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 12)")
        await asyncio.sleep(2)
        await self.page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()
        await asyncio.sleep(2)
        await self.page.locator("svg.Octicon-sc-9kayk9-0").nth(1).click()
        await asyncio.sleep(2)
        await self.page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(2)

        # Navigate back to pytorch/pytorch
        await self.page.locator(
            'a[data-pjax="#repo-content-pjax-container"][data-turbo-frame="repo-content-turbo-frame"][href="/pytorch/pytorch"]'
        ).nth(1).click()
        await asyncio.sleep(2)

    def __str__(self):
        return "GithubNormalWorkflow"

    def __repr__(self):
        return "GithubNormalWorkflow()"
