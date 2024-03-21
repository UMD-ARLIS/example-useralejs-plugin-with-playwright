import asyncio
from abc import ABC
from abc import abstractmethod

from playwright.async_api import Page


class Workflow(ABC):
    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    async def run(self) -> None:
        pass

    async def loop(self) -> None:
        """
        Run the workflow in an infinite loop.
        """
        while True:
            await self.run()
            await asyncio.sleep(2)
