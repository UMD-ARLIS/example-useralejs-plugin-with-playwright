import asyncio
import json
import logging
from argparse import Namespace
from typing import Any
from typing import Dict

from bot.lib.run import run
from bot.workflows.utils import import_workflow
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_args(input_args=None) -> Namespace:
    import argparse

    def parse_dict(s: str) -> Dict[str, Any]:
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            raise argparse.ArgumentTypeError(f"Invalid json string provided. \n{e}")

    parser = argparse.ArgumentParser(description="Run UserALE logging workflows")
    parser.add_argument(
        "--workflow_type",
        type=str,
        help="The type of workflow to run",
        # Add more workflow types here as needed,
        # eventually cardinality will be too high for choices
        choices=[
            "github-anomalous",
            "github-normal",
        ],
        required=True,
    )
    parser.add_argument(
        "--mode",
        type=str,
        help="The mode in which to run the workflow",
        choices=["run", "loop"],
        default="run",
        required=False,
    )
    parser.add_argument(
        "--use_plugin",
        action="store_true",
        help="Whether to use the UserALE browser plugin. Useful when the application under test is not instrumented in the source code.",
    )
    parser.add_argument(
        "--kwargs",
        type=parse_dict,
        help="Additional keyword arguments for the workflow. Must be a JSON string.",
        default={},
        required=False,
    )
    if input_args is not None:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()

    # Logging the arguments
    logging.info("Arguments for this run:")
    for arg, value in vars(args).items():
        logging.info(f"  - {arg.replace('_', ' ').title()}: {value}")

    return args


async def main(args: Namespace):
    logger.info(
        f"\tWorkflow type: {args.workflow_type}"
        f"\tMode: {args.mode}"
        f"\tUse UserALE browser plugin: {args.use_plugin}"
        f"\tArguments: {args.kwargs}"
    )
    workflow = import_workflow(workflow_type=args.workflow_type)

    # Add any additional keyword arguments here

    # Run the workflow
    async with async_playwright() as p:
        await run(
            p,
            workflow=workflow,
            mode=args.mode,
            use_plugin=args.use_plugin,
            logger=logger,
            **args.kwargs,
        )


if __name__ == "__main__":
    logger.info("Starting UserALE Workflow bot")
    args = parse_args()
    asyncio.run(main(args=args))
