import asyncio
import logging

from playwright.async_api import async_playwright
from src import run


from src.workflows.utils import import_workflow

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="Run UserALE logging workflows")
    parser.add_argument(
        "workflow_type",
        type=str,
        help="The type of workflow to run",
        # Add more workflow types here as needed,
        # eventually cardinality will be too high for choices
        choices=[
            "github-anomalous",
            "github-plugin",
        ],
    )
    parser.add_argument(
        "mode",
        type=str,
        help="The mode in which to run the workflow",
        choices=["run", "loop"],
        default="run",
        required=False,
    )
    args = parser.parse_args()

    # Logging the arguments
    logging.info("Arguments for this run:")
    for arg, value in vars(args).items():
        logging.info(f"  - {arg.replace('_', ' ').title()}: {value}")

    return args


async def main(args):
    logger.info(f"\tWorkflow type: {args.workflow_type}" f"\tMode: {args.mode}")
    workflow = import_workflow(workflow_type=args.workflow_type)

    # Run the workflow
    async with async_playwright() as p:
        await run(p, workflow=workflow, mode=args.mode, logger=logger)


if __name__ == "__main__":
    logger.info("Starting UserALE Workflow bot")
    args = parse_args()
    asyncio.run(main(args=args))
