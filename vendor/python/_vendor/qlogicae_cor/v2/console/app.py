from __future__ import annotations

from typing import Any

_version: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _version

    from importlib.metadata import version

    _version = (
        version
    )

    _handle_dynamic_imports = lambda: None


def main() -> None:
    _handle_dynamic_imports()

    print(
        _version("qlogicae-cor")
    )
