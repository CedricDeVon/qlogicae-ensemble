from __future__ import annotations

__all__ = (
    "SystemManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

_os: Any = None
_platform: Any = None
_path: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _os
    global _platform
    global _path

    import os
    import pathlib
    import platform

    _os = os
    _platform = platform
    _path = pathlib.Path

    _handle_dynamic_imports = lambda: None


class SystemManager:
    __slots__ = (
        "_original_executing_console_filesystem_path",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._original_executing_console_filesystem_path = (
            f"{_path.cwd().resolve()}"
        )

    @property
    def original_executing_console_filesystem_path(
        self,
    ) -> str:
        return self._original_executing_console_filesystem_path

    @property
    def current_executing_script_filesystem_path(
        self,
    ) -> str:
        return f"{_path(__file__).resolve()}"

    @property
    def current_executing_console_filesystem_path(
        self,
    ) -> str:
        return f"{_path.cwd().resolve()}"

    @current_executing_console_filesystem_path.setter
    def current_executing_console_filesystem_path(
        self,
        filesystem_path: str,
    ) -> None:
        path: Path = (
            _path(filesystem_path)
            .expanduser()
            .resolve()
        )

        if not path.exists():
            raise ValueError(
                f"directory '{path}' does not exist",
            )

        if not path.is_dir():
            raise ValueError(
                f"'{path}' is not a directory",
            )

        _os.chdir(path)

    @property
    def operating_system_name(self) -> str:
        value: str = _platform.system()

        return value

    @property
    def operating_system_architecture(
        self,
    ) -> str:
        value: str = _platform.machine()

        return value
