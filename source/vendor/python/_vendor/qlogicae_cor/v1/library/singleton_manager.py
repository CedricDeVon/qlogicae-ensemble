from collections.abc import Callable
from typing import Any, TypeVar, cast

from qlogicae_cor.v1.library.singleton_manager_configurations import (
    SingletonManagerConfigurations,
)

Type = TypeVar("Type")


class SingletonManager:
    _configurations: SingletonManagerConfigurations = SingletonManagerConfigurations()

    _singletons: dict[
        Callable[[], Any],
        Any,
    ] = {}

    _singleton_arrays: dict[
        Callable[[], Any],
        list[Any],
    ] = {}

    @classmethod
    def setup(
        self,
        new_configurations: SingletonManagerConfigurations,
    ) -> bool:
        if self._configurations.is_disabled_for_handling(
            new_configurations is None,
        ):
            return False

        self._configurations = new_configurations

        return True

    @classmethod
    def reset(
        self,
    ) -> bool:
        if self._configurations.is_disabled_for_handling():
            return False

        self._configurations = SingletonManagerConfigurations()

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
            raise ValueError("error at 'qlogicae-cor' - something went wrong here")

        instances = self._singleton_arrays.get(
            constructor,
        )

        if instances is None:
            instances = [constructor() for _ in range(instance_count)]

            self._singleton_arrays[constructor] = instances

        return cast(Type, instances[abs(index) % instance_count])

