import asyncio
import os
from typing import Literal, List
from enum import Enum
from bot.lib.const import TIMEOUT_MS
from bot.lib.workflow import Workflow
from playwright.async_api import Page
from pydantic import BaseModel, EmailStr


class RolesEnum(str, Enum):
    Admin = "1"
    Public = "2"
    Alpha = "3"
    Gamma = "4"
    SqlLab = "5"


ACTIVE = Literal["y", "n"]


class SupersetUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    active: ACTIVE
    conf_password: str
    password: str
    roles: List[RolesEnum]


class SupersetWorkflow(Workflow):
    def __init__(self, page: Page, **kwargs):
        super().__init__(page=page)

        # Extract user login credentials from kwargs
        # NOTE: This will throw if the user is not provided which is what we want
        self.user = SupersetUser.model_validate(kwargs.pop("user"))
        self.base_url = kwargs.pop("superset_url", "http://localhost:8088")

    def url(self, url_path):
        return os.path.join(self.base_url, url_path)

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    async def run(self) -> None:
        pass

    async def login(self) -> None:
        await self.page.goto(self.url("login/"))
        await self.page.wait_for_timeout(TIMEOUT_MS)

        # Fill in username and password
        await self.page.locator('input[name="username"]').fill(self.user.username)
        await self.page.locator('input[name="password"]').fill(self.user.password)

        # Click login button
        await self.page.locator('input[type="submit"]').click()
        await self.page.wait_for_timeout(TIMEOUT_MS)


class SupersetGraphInexperiencedWorkflow(SupersetWorkflow):
    async def run(self):
        await self.login()

        #
        # Detour: investigate the COVID Vaccine Dashboard
        #
        await self.page.get_by_text("COVID Vaccine Dashboard").click()
        await self.page.mouse.wheel(0, 600)
        await asyncio.sleep(15)
        await self.page.mouse.wheel(0, -600)

        #
        # Return to workflow
        #
        # Go to charts page
        await self.page.locator('a[role="button"]', has_text="Charts").click()
        await self.page.wait_for_timeout(TIMEOUT_MS)

        #
        # Detour: scroll down, select chart, view, return
        #
        await self.page.mouse.wheel(0, 300)
        await self.page.get_by_text("Vaccine Candidates per Approach & Stage").click()
        await asyncio.sleep(15)
        await self.page.go_back()
        await self.page.wait_for_timeout(TIMEOUT_MS)

        #
        # Return to workflow
        #
        # Create new chart
        await self.page.locator('button[type="button"]', has_text="Chart").click()
        await self.page.wait_for_timeout(TIMEOUT_MS)

        # Select covid_vaccines dataset
        await self.page.locator('input[aria-label="Dataset"]').fill("covid_vaccines")
        await self.page.locator('div[label="covid_vaccines"]').click()
        await asyncio.sleep(5)

        #
        # Detour: click on a number of filters before KPI
        #
        for item in ["Correlation", "Distribution", "Evolution", "KPI"]:
            await self.page.locator(f'button[name="{item}"]', has_text=item).click()
            await asyncio.sleep(7)

        # select KPI as filter
        await self.page.locator('button[name="KPI"]', has_text="KPI").click()
        await asyncio.sleep(5)

        # select funnel chart
        await self.page.locator('div[role="button"]', has_text="Funnel Chart").click()
        await asyncio.sleep(5)

        # create new chart
        await self.page.locator(
            'button[type="button"]', has_text="Create new chart"
        ).click()
        await self.page.wait_for_timeout(TIMEOUT_MS)

        #
        # Detour: Examine page for quite a whilew
        #
        await asyncio.sleep(15)

        # select dimensions > saved TAB > clinical_stage
        await self.page.locator(
            'xpath=//*[@id="controlSections-panel-query"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div'
        ).click()
        await self.page.locator('input[aria-label="Saved expressions"]').click()
        await self.page.locator('div[label="clinical_stage"]').click()
        await self.page.locator(
            'xpath=//*[@id="metrics-edit-popover"]/div[2]/button[2]'
        ).click()
        await asyncio.sleep(5)

        #
        # Detour: Hover over info icon
        #
        await self.page.locator('div[class="metrics-select"]').hover()
        await asyncio.sleep(5)

        # METRIC > saved TAB > count
        await self.page.locator(
            'xpath=//*[@id="controlSections-panel-query"]/div/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div'
        ).click()
        await self.page.locator('input[aria-label="Select saved metrics"]').click()
        await self.page.locator('div[label="count"]').click()
        await self.page.locator(
            'xpath=//*[@id="metrics-edit-popover"]/div[2]/button[2]'
        ).click()
        await asyncio.sleep(5)

        # Create chart
        await self.page.locator(
            'button[type="button"]', has_text="Create chart"
        ).click()
        await asyncio.sleep(10)

        # Add naame
        await self.page.locator('input[aria-label="Chart title"]').fill(
            "Covid Vaccine Clinical Stage Funnel Chart"
        )
        await asyncio.sleep(10)

        # click ... menu > share > copy permalink to clipboard
        await self.page.locator('button[aria-label="Menu actions trigger"]').click()
        await self.page.get_by_title("Share").hover()
        await self.page.get_by_text("Copy permalink to clipboard").click()  ##

    def __str__(self):
        return "SupersetGraphInexperiencedWorkflow"

    def __repr__(self):
        return "SupersetGraphInexperiencedWorkflow()"


class SupersetGraphExperiencedWorkflow(SupersetWorkflow):
    async def run(self):
        await self.login()

        await self.page.locator('a[role="button"]', has_text="Charts").click()
        await asyncio.sleep(1)

        # Create new chart
        await self.page.locator('button[type="button"]', has_text="Chart").click()
        await asyncio.sleep(1)

        # Select covid_vaccines dataset
        await self.page.locator('input[aria-label="Dataset"]').fill("covid_vaccines")
        await self.page.locator('div[label="covid_vaccines"]').click()
        await asyncio.sleep(1)

        # select KPI as filter
        await self.page.locator('button[name="KPI"]', has_text="KPI").click()
        await asyncio.sleep(1)

        # select funnel chart
        await self.page.locator('div[role="button"]', has_text="Funnel Chart").click()
        await asyncio.sleep(1)

        # create new chart
        await self.page.locator(
            'button[type="button"]', has_text="Create new chart"
        ).click()
        await self.page.wait_for_timeout(TIMEOUT_MS)

        # select dimensions > saved TAB > clinical_stage
        await self.page.locator(
            'xpath=//*[@id="controlSections-panel-query"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div'
        ).click()
        await self.page.locator('input[aria-label="Saved expressions"]').click()
        await self.page.locator('div[label="clinical_stage"]').click()
        await self.page.locator(
            'xpath=//*[@id="metrics-edit-popover"]/div[2]/button[2]'
        ).click()
        await asyncio.sleep(1)

        # METRIC > saved TAB > count
        await self.page.locator(
            'xpath=//*[@id="controlSections-panel-query"]/div/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div'
        ).click()
        await self.page.locator('input[aria-label="Select saved metrics"]').click()
        await self.page.locator('div[label="count"]').click()
        await self.page.locator(
            'xpath=//*[@id="metrics-edit-popover"]/div[2]/button[2]'
        ).click()
        await asyncio.sleep(1)

        # Create chart
        await self.page.locator(
            'button[type="button"]', has_text="Create chart"
        ).click()
        await asyncio.sleep(5)

        # Add naame
        await self.page.locator('input[aria-label="Chart title"]').fill(
            "Covid Vaccine Clinical Stage Funnel Chart"
        )
        await asyncio.sleep(1)

        # click ... menu > share > copy permalink to clipboard
        await self.page.locator('button[aria-label="Menu actions trigger"]').click()
        await self.page.get_by_title("Share").hover()
        await self.page.get_by_text("Copy permalink to clipboard").click()

    def __str__(self):
        return "SupersetGraphExperiencedWorkflow"

    def __repr__(self):
        return "SupersetGraphExperiencedWorkflow()"
