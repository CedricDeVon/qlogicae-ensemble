from __future__ import annotations

from typing import Any

_json: Any = None
_singleton_manager: Any = None
_json_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _json
    global _singleton_manager
    global _json_manager

    import json

    import qlogicae_cor.v1.library.json_manager
    import qlogicae_cor.v1.library.singleton_manager

    _json = json
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _json_manager = (
        qlogicae_cor.v1.library.json_manager.JsonManager
    )

    _handle_dynamic_imports = lambda: None


class JsonTextManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

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
        manager: _json_manager = (
            _singleton_manager.get_singleton(
                _json_manager,
            )
        )

        result: str = _json.dumps(
            value,
            indent=manager.indent_count,
            ensure_ascii=manager.is_ascii_format_enabled,
        )

        return result
