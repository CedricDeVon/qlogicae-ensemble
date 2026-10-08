from __future__ import annotations

__all__ = (
    "ValueCacheManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .target_cache_value import TargetCacheValue

_FilesystemManager: Any = None
_SingletonManager: Any = None
_TargetCacheValue: Any = None
_ValueCacheStorageManager: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _FilesystemManager
    global _SingletonManager
    global _TargetCacheValue
    global _ValueCacheStorageManager

    from .filesystem_manager import FilesystemManager
    from .singleton_manager import SingletonManager
    from .target_cache_value import TargetCacheValue
    from .value_cache_storage_manager import ValueCacheStorageManager

    _FilesystemManager = (
        FilesystemManager
    )
    _SingletonManager = (
        SingletonManager
    )
    _TargetCacheValue = (
        TargetCacheValue
    )
    _ValueCacheStorageManager = (
        ValueCacheStorageManager
    )

    _handle_dynamic_imports = lambda: None


class ValueCacheManager:
    __slots__ = (
        "_filesystem_manager",
        "_value_cache_storage_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._filesystem_manager = (
            _SingletonManager.get_singleton(
                _FilesystemManager
            )
        )
        self._value_cache_storage_manager = (
            _SingletonManager.get_singleton(
                _ValueCacheStorageManager
            )
        )

    def is_key_found(
        self,
        key_path: tuple[str | int, ...],
    ) -> bool:
        result: bool = self._value_cache_storage_manager.is_key_found(key_path)

        return result

    def get_one_value(
        self,
        key_path: tuple[str | int, ...],
        output_type: TargetCacheValue | None = None,
    ) -> object:
        if output_type is None:
            output_type = _TargetCacheValue.DEFINED

        value = self._value_cache_storage_manager.get_one_value(key_path)

        self.throw_if_value_is_explicitly_invalid(
            value,
            output_type,
        )

        return value

    def set_one_value(
        self,
        key_path: tuple[str | int, ...],
        value: object,
        output_type: TargetCacheValue | None = None,
    ) -> bool:
        if output_type is None:
            output_type = _TargetCacheValue.DEFINED

        self.throw_if_value_is_explicitly_invalid(
            value,
            output_type,
        )

        result: bool = self._value_cache_storage_manager.set_one_value(
            key_path,
            value,
        )

        return result

    def remove_one_value(
        self,
        key_path: tuple[str | int, ...],
    ) -> bool:
        self.throw_if_key_not_found(key_path)

        result: bool = self._value_cache_storage_manager.remove_one_value(key_path)

        return result

    def clear_all_values(self) -> bool:
        result: bool = self._value_cache_storage_manager.clear_all_values()

        return result

    def display_all_items(self) -> bool:
        result: bool = self._value_cache_storage_manager.display_all_items()

        return result

    def throw_if_value_is_explicitly_invalid(
        self,
        value: object,
        output_type: TargetCacheValue | None = None,
    ) -> bool:
        if output_type is None:
            output_type = _TargetCacheValue.DEFINED

        match output_type:
            case _TargetCacheValue.FILESYSTEM_PATH:
                self._filesystem_manager.throw_if_filesystem_path_invalid(
                    value,
                )

                return True

            case _TargetCacheValue.FILE_PATH:
                self._filesystem_manager.throw_if_file_path_invalid(
                    value,
                )

                return True

            case _TargetCacheValue.FOLDER_PATH:
                self._filesystem_manager.throw_if_folder_path_invalid(
                    value,
                )

                return True

            case _TargetCacheValue.DEFINED:
                self.throw_if_undefined(value)

                return True

            case _:
                return False

    def throw_if_key_not_found(
        self,
        key_path: tuple[str | int, ...],
    ) -> bool:
        if not self._value_cache_storage_manager.is_key_found(key_path):
            raise KeyError(
                f"key path '{key_path}' does not exist",
            )

        return False

    def throw_if_undefined(
        self,
        value: Any,
    ) -> bool:
        if value is None:
            raise KeyError("value is not defined")

        return False
