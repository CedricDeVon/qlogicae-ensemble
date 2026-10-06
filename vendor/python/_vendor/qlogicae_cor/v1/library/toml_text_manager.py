from __future__ import annotations

from typing import Any

_tomllib: Any = None
_tomli_w: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _tomllib
    global _tomli_w

    import tomllib

    import tomli_w

    _tomllib = tomllib
    _tomli_w = tomli_w

    _handle_dynamic_imports = lambda: None


class TomlTextManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def is_valid(
        self,
        value: str,
    ) -> bool:
        _tomllib.loads(value)

        return True

    def convert_to_object(
        self,
        value: str,
    ) -> object:
        result: object = _tomllib.loads(value)

        return result

    def convert_to_string(
        self,
        value: Any,
    ) -> str:
        result: str = _tomli_w.dumps(value)

        return result
