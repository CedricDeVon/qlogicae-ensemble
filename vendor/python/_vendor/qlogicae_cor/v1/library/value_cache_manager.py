from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.target_cache_value import TargetCacheValue

_filesystem_manager: Any = None
_singleton_manager: Any = None
_target_cache_value: Any = None
_value_cache_storage_manager: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _filesystem_manager
    global _singleton_manager
    global _target_cache_value
    global _value_cache_storage_manager

    import qlogicae_cor.v1.library.filesystem_manager
    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.target_cache_value
    import qlogicae_cor.v1.library.value_cache_storage_manager

    _filesystem_manager = (
        qlogicae_cor.v1.library.filesystem_manager.FilesystemManager
    )
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _target_cache_value = (
        qlogicae_cor.v1.library.target_cache_value.TargetCacheValue
    )
    _value_cache_storage_manager = (
        qlogicae_cor.v1.library.value_cache_storage_manager.ValueCacheStorageManager
    )

    _handle_dynamic_imports = lambda: None


class ValueCacheManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def is_key_found(
        self,
        keys: tuple[str | int, ...],
    ) -> bool:
        result: bool = _singleton_manager.get_singleton(
            _value_cache_storage_manager,
        ).is_key_found(keys)

        return result

    def get_one_value(
        self,
        keys: tuple[str | int, ...],
        output_type: TargetCacheValue | None = None,
    ) -> object:
        if output_type is None:
            output_type = _target_cache_value.DEFINED

        value = _singleton_manager.get_singleton(
            _value_cache_storage_manager,
        ).get_one_value(keys)

        self.throw_if_value_is_explicitly_invalid(
            value,
            output_type,
        )

        return value

    def set_one_value(
        self,
        keys: tuple[str | int, ...],
        value: object,
        output_type: TargetCacheValue | None = None,
    ) -> bool:
        if output_type is None:
            output_type = _target_cache_value.DEFINED

        self.throw_if_value_is_explicitly_invalid(
            value,
            output_type,
        )

        result: bool = _singleton_manager.get_singleton(
            _value_cache_storage_manager,
        ).set_one_value(
            keys,
            value,
        )

        return result

    def remove_one_value(
        self,
        keys: tuple[str | int, ...],
    ) -> bool:
        self.throw_if_key_not_found(keys)

        result: bool = _singleton_manager.get_singleton(
            _value_cache_storage_manager,
        ).remove_one_value(keys)

        return result

    def clear_all_values(self) -> bool:
        result: bool = _singleton_manager.get_singleton(
            _value_cache_storage_manager,
        ).clear_all_values()

        return result

    def display_all_items(self) -> bool:
        result: bool = _singleton_manager.get_singleton(
            _value_cache_storage_manager,
        ).display_all_items()

        return result

    def throw_if_value_is_explicitly_invalid(
        self,
        value: object,
        output_type: TargetCacheValue | None = None,
    ) -> bool:
        if output_type is None:
            output_type = _target_cache_value.DEFINED

        filesystem_manager = (
            _singleton_manager.get_singleton(
                _filesystem_manager,
            )
        )

        match output_type:
            case _target_cache_value.FILESYSTEM_PATH:
                filesystem_manager.throw_if_filesystem_path_invalid(
                    value,
                )

                return True

            case _target_cache_value.FILE_PATH:
                filesystem_manager.throw_if_file_path_invalid(
                    value,
                )

                return True

            case _target_cache_value.FOLDER_PATH:
                filesystem_manager.throw_if_folder_path_invalid(
                    value,
                )

                return True

            case _target_cache_value.DEFINED:
                self.throw_if_undefined(value)

                return True

            case _:
                return False

    def throw_if_key_not_found(
        self,
        keys: tuple[str | int, ...],
    ) -> bool:
        if not _singleton_manager.get_singleton(
            _value_cache_storage_manager,
        ).is_key_found(keys):
            raise KeyError(
                f"key path '{keys}' does not exist",
            )

        return False

    def throw_if_undefined(
        self,
        value: Any,
    ) -> bool:
        if value is None:
            raise KeyError("value is not defined")

        return False
