from __future__ import annotations

__all__ = (
    "ObjectMergeManager",
)

from typing import Any

_deepcopy: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _deepcopy

    from copy import deepcopy

    _deepcopy = deepcopy

    _handle_dynamic_imports = lambda: None


class ObjectMergeManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def deep_merge(
        self,
        left: object,
        right: object,
    ) -> object:
        if left is None:
            return _deepcopy(right)

        if right is None:
            return _deepcopy(left)

        if isinstance(left, dict) and isinstance(right, dict):
            result = _deepcopy(left)

            for key, value in right.items():
                if key in result:
                    result[key] = self.deep_merge(
                        result[key],
                        value,
                    )
                else:
                    result[key] = _deepcopy(value)

            return result

        if isinstance(left, list) and isinstance(right, list):
            return _deepcopy(left) + _deepcopy(right)

        return _deepcopy(right)

    def deep_merge_fragments(
        self,
        left: object,
        right: object,
    ) -> object:
        if left is None:
            return _deepcopy(right)

        if right is None:
            return _deepcopy(left)

        if isinstance(left, dict) and isinstance(right, dict):
            result = _deepcopy(left)

            for key, value in right.items():
                if key in result:
                    result[key] = self.deep_merge_fragments(
                        result[key],
                        value,
                    )
                else:
                    result[key] = _deepcopy(value)

            return result

        if isinstance(left, list) and isinstance(right, list):
            return _deepcopy(right)

        return _deepcopy(right)
