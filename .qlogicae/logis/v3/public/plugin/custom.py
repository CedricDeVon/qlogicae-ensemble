from __future__ import annotations

from typing import Any

import time

def run_command(**kwargs: Any) -> Any:
    if not kwargs:
        return 0

    a = (kwargs.get("a", 0) or 0)
    b = (kwargs.get("b", 0) or 0)

    return a + b


def run_time_now() -> Any:
    return f"{time.time_ns()}"


command = {
    "public-a": {
        "value": run_command
    }
}

macros = {
    "static": {
        "file": {
            "targets": {
                "public-a": {
                    "value": "public | ${{ qlogicae-logis-base-description }} | ${{ public-time-now }} | ${{ public-time-now }}"
                },
                "public-b": {
                    "value": "public-a | ${{ public-a }}"
                }
            }
        }
    },
    "dynamic": {
        "targets": {
            "public-time-now": {
                "value": run_time_now
            }
        }
    }
}

