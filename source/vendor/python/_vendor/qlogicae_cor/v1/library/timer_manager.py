from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.time_unit import TimeUnit

_singleton_manager: Any = None
_time_manager: Any = None
_time_unit: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _singleton_manager
    global _time_manager
    global _time_unit

    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.time_manager
    import qlogicae_cor.v1.library.time_unit

    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _time_manager = (
        qlogicae_cor.v1.library.time_manager.TimeManager
    )
    _time_unit = (
        qlogicae_cor.v1.library.time_unit.TimeUnit
    )

    _handle_dynamic_imports = lambda: None


class TimerManager:
    __slots__ = (
        "_start_timestamp",
        "_stop_timestamp",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._start_timestamp: float = 0
        self._stop_timestamp: float = 0

    @property
    def start_timestamp(self) -> float:
        return self._start_timestamp

    @property
    def stop_timestamp(self) -> float:
        return self._stop_timestamp

    def start_time(self) -> bool:
        self._start_timestamp = (
            _singleton_manager.get_singleton(
                _time_manager,
            ).current_nanosecond
        )

        return True

    def stop_time(self) -> bool:
        self._stop_timestamp = (
            _singleton_manager.get_singleton(
                _time_manager,
            ).current_nanosecond
        )

        return True

    def clear_time(self) -> bool:
        self._start_timestamp = 0
        self._stop_timestamp = 0

        return True

    def reset_time(self) -> bool:
        self._start_timestamp = (
            _singleton_manager.get_singleton(
                _time_manager,
            ).current_nanosecond
        )
        self._stop_timestamp = 0

        return True

    def calculate_elapsed_time(
        self,
        time_unit: TimeUnit | None = None,
    ) -> float:
        if time_unit is None:
            time_unit = _time_unit.SECOND

        manager = _singleton_manager.get_singleton(
            _time_manager,
        )

        value: float = manager.convert_time_unit(
            manager.current_nanosecond - self._start_timestamp,
            output_time_unit=time_unit,
        )

        return value

    def calculate_duration_time(
        self,
        time_unit: TimeUnit | None = None,
    ) -> float:
        if time_unit is None:
            time_unit = _time_unit.SECOND

        manager = _singleton_manager.get_singleton(
            _time_manager,
        )

        value: float = manager.convert_time_unit(
            self._stop_timestamp - self._start_timestamp,
            output_time_unit=time_unit,
        )

        return value
