from __future__ import annotations

from typing import Any

_version: Any = None
_ConsoleDisplayManager: Any = None
_SingletonManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _ConsoleDisplayManager
    global _SingletonManager
    global _version

    from importlib.metadata import version

    from qlogicae_cor.v1.library import console_display_manager, singleton_manager

    _ConsoleDisplayManager = (
        console_display_manager.ConsoleDisplayManager
    )
    _SingletonManager = (
        singleton_manager.SingletonManager
    )
    _version = (
        version
    )

    _handle_dynamic_imports = lambda: None


def main() -> None:
    _handle_dynamic_imports()

    _SingletonManager.get_singleton(
        _ConsoleDisplayManager,
    ).render_one_component(
        _version("qlogicae-cor")
    )
