from __future__ import annotations

from collections.abc import Hashable, Mapping, Sequence

__all__ = (
    "GroupSelectionManager"
)

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports

    _handle_dynamic_imports = lambda: None


class GroupSelectionManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def flatten_group(
        self,
        target: Hashable,
        data: Mapping[Hashable, Sequence[Hashable]],
    ) -> tuple[Hashable, ...]:
        resolved: list[Hashable] = []
        visited: set[Hashable] = set()
        stack: list[Hashable] = [target]

        while stack:
            value = stack.pop()
            if value in visited:
                continue

            visited.add(value)

            if value not in data:
                resolved.append(value)
                continue

            stack.extend(reversed(data[value]))

        return tuple(resolved)
