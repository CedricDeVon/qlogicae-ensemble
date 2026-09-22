from __future__ import annotations

from typing import Any

import time

def run_command(**kwargs: Any) -> Any:
    a = kwargs.get("a", 0)
    b = kwargs.get("b", 0)

    return a + b


def run_time_now() -> Any:
    return f"{time.time_ns()}"


DATA: dict[str, dict[str, Any]]= {
    "commands": {
        "public-a": {
            "value": run_command
        }
    },
    "macros": {
        "static": {
            "public-a": {
                "value": "public | ${{ qlogicae-logis-base-description }} | ${{ public-time-now }} | ${{ public-time-now }}"
            },
            "public-b": {
                "value": "public-a | ${{ public-a }}"
            }

        },
        "dynamic": {
            "public-time-now": {
                "value": run_time_now
            }
        }
    },
}

METADATA: dict[str, dict[str, Any]] = {    

}
