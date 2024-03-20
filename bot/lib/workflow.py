import asyncio
from abc import ABC, abstractmethod
from playwright.async_api import Page


class Workflow(ABC):
    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    async def run(self):
        pass

    async def loop(self):
        """
        Run the workflow in an infinite loop.
        """
        while True:
            await self.run()
            await asyncio.sleep(2)
