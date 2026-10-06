from __future__ import annotations

from typing import Any

_Path: Any = None
_tomllib: Any = None
_tomli_w: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _Path
    global _tomllib
    global _tomli_w

    import tomllib
    from pathlib import Path

    import tomli_w

    _Path = Path
    _tomllib = tomllib
    _tomli_w = tomli_w

    _handle_dynamic_imports = lambda: None


class TomlFileIoManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def read_file(
        self,
        file_path: str,
    ) -> Any:
        path = _Path(file_path)

        output_data: Any = {}

        with path.open("rb") as file:
            output_data = _tomllib.load(file)

        return output_data

    def write_file(
        self,
        file_path: str,
        data: Any,
    ) -> bool:
        path = _Path(file_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open("wb") as file:
            _tomli_w.dump(
                data,
                file,
            )

        return True
