from typing import Literal

RunMode = Literal["run", "loop"]
WorkflowType = Literal[
    "github-anomalous",
    "github-normal",
    "superset-graph-experienced",
    "superset-graph-inexperienced",
]
