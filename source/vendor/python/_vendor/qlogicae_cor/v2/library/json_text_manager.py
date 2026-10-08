from __future__ import annotations

__all__ = (
    "JsonTextManager",
)

from typing import Any

_json: Any = None
_SingletonManager: Any = None
_JsonManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _json
    global _SingletonManager
    global _JsonManager

    import json

    from .json_manager import JsonManager
    from .singleton_manager import SingletonManager

    _json = json
    _SingletonManager = (
        SingletonManager
    )
    _JsonManager = (
        JsonManager
    )

    _handle_dynamic_imports = lambda: None


class JsonTextManager:
    __slots__ = (
        "_json_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._json_manager = _SingletonManager.get_singleton(
            _JsonManager
        )

    def is_valid(
        self,
        value: str,
    ) -> bool:
        _json.loads(value)

        return True

    def convert_to_object(
        self,
        value: str,
    ) -> Any:
        return _json.loads(value)

    def convert_to_string(
        self,
        value: Any,
    ) -> str:
        result: str = _json.dumps(
            value,
            indent=self._json_manager.indent_count,
            ensure_ascii=self._json_manager.is_ascii_format_enabled,
        )

        return result
