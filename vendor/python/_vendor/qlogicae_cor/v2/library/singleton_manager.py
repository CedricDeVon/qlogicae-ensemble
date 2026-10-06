from collections.abc import Callable
from typing import Any, TypeVar, cast

__all__ = (
    "SingletonManager",
)

Type = TypeVar("Type")


class SingletonManager:
    _singletons: dict[
        Callable[[], Any],
        Any,
    ] = {}

    _singleton_arrays: dict[
        Callable[[], Any],
        list[Any],
    ] = {}

    @classmethod
    def reset(
        self,
    ) -> bool:
        self._singletons.clear()
        self._singleton_arrays.clear()

        return True

    @classmethod
    def get_singleton(
        self,
        constructor: Callable[[], Type],
    ) -> Type:
        instance = self._singletons.get(constructor)

        if instance is None:
            instance = constructor()
            self._singletons[constructor] = instance

        return instance

    @classmethod
    def get_singleton_from_pool(
        self,
        constructor: Callable[[], Type],
        instance_count: int,
        index: int,
    ) -> Type:
        if instance_count <= 0:
            raise ValueError("something went wrong here")

        instances = self._singleton_arrays.get(
            constructor,
        )

        if instances is None:
            instances = [constructor() for _ in range(instance_count)]

            self._singleton_arrays[constructor] = instances

        return cast(Type, instances[abs(index) % instance_count])

