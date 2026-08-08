from __future__ import annotations

from typing import Any

def run_command(**kwargs: Any) -> Any:
    a = kwargs.get("a", 0)
    b = kwargs.get("b", 0)

    return a - b
