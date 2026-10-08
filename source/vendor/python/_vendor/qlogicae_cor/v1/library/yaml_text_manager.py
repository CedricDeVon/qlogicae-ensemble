from __future__ import annotations

from typing import Any

_yaml: Any = None
_singleton_manager: Any = None
_yaml_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _yaml
    global _singleton_manager
    global _yaml_manager

    import yaml

    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.yaml_manager

    _yaml = yaml
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _yaml_manager = (
        qlogicae_cor.v1.library.yaml_manager.YamlManager
    )

    _handle_dynamic_imports = lambda: None


class YamlTextManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def is_valid(
        self,
        value: str,
    ) -> bool:
        _yaml.safe_load(value)

        return True

    def convert_to_object(
        self,
        value: str,
    ) -> Any:
        return _yaml.safe_load(value)

    def convert_to_string(
        self,
        value: Any,
    ) -> str:
        manager = (
            _singleton_manager.get_singleton(
                _yaml_manager,
            )
        )

        result: str = _yaml.safe_dump(
            value,
            sort_keys=manager.is_key_sorting_enabled,
            default_flow_style=manager.is_default_flow_state_enabled,
            allow_unicode=manager.is_unicode_enabled,
            indent=manager.indent_count,
        )

        return result
