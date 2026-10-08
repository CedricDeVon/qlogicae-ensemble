from __future__ import annotations

__all__ = (
    "TimeManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .time_unit import TimeUnit

_time: Any = None
_date: Any = None
_datetime: Any = None
_SingletonManager: Any = None
_TimeUnit: Any = None
_TimeZoneManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _time
    global _date
    global _datetime
    global _SingletonManager
    global _TimeUnit
    global _TimeZoneManager

    import time
    from datetime import date, datetime

    from .singleton_manager import SingletonManager
    from .time_unit import TimeUnit
    from .time_zone_manager import (
        TimeZoneManager,
    )

    _time = time
    _date = date
    _datetime = datetime
    _SingletonManager = SingletonManager
    _TimeUnit = TimeUnit
    _TimeZoneManager = TimeZoneManager

    _handle_dynamic_imports = lambda: None


class TimeManager:
    __slots__ = (
        "_TIME_UNIT_TO_NANOSECONDS",
        "_time_zone_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._TIME_UNIT_TO_NANOSECONDS: dict[
            TimeUnit,
            float,
        ] = {
            _TimeUnit.NANOSECOND: 1.0,
            _TimeUnit.MICROSECOND: 1e3,
            _TimeUnit.MILLISECOND: 1e6,
            _TimeUnit.SECOND: 1e9,
            _TimeUnit.MINUTE: 60e9,
            _TimeUnit.HOUR: 3600e9,
            _TimeUnit.DAY: 86400e9,
            _TimeUnit.WEEK: 604800e9,
            _TimeUnit.MONTH: 2629746e9,
            _TimeUnit.YEAR: 31556952e9,
            _TimeUnit.DECADE: 315569520e9,
            _TimeUnit.CENTURY: 3155695200e9,
            _TimeUnit.MILLENNIUM: 31556952000e9,
        }

        self._time_zone_manager = (
            _SingletonManager.get_singleton(
                _TimeZoneManager
            )
        )

    @property
    def current_iso8601_date(self) -> str:
        value: str = _date.today().strftime(
            "%Y-%m-%d",
        )

        return value

    @property
    def current_nanosecond(self) -> int:
        value: int = _time.time_ns()

        return value

    @property
    def current_microsecond(self) -> int:
        return self.current_nanosecond // 1_000

    @property
    def current_millisecond(self) -> int:
        return self.current_nanosecond // 1_000_000

    @property
    def current_second(self) -> int:
        value: int = _datetime.now(
            self._time_zone_manager
                .selected_time_zone,
        ).second

        return value

    @property
    def current_minute(self) -> int:
        value: int = _datetime.now(
            self._time_zone_manager
                .selected_time_zone,
        ).minute

        return value

    @property
    def current_hour(self) -> int:
        value: int = _datetime.now(
            self._time_zone_manager
                .selected_time_zone,
        ).hour

        return value

    @property
    def current_day(self) -> int:
        value: int = _datetime.now(
            self._time_zone_manager
                .selected_time_zone,
        ).day

        return value

    @property
    def current_week(self) -> int:
        value: int = _datetime.now().isocalendar().week

        return value

    @property
    def current_month(self) -> int:
        value: int = _datetime.now(
            self._time_zone_manager
                .selected_time_zone,
        ).month

        return value

    @property
    def current_year(self) -> int:
        value: int = _datetime.now(
            self._time_zone_manager
                .selected_time_zone,
        ).year

        return value

    @property
    def current_decade(self) -> int:
        return self.current_year // 10

    @property
    def current_century(self) -> int:
        return (
            self.current_year - 1
        ) // 100 + 1

    @property
    def current_millenium(self) -> int:
        return (
            self.current_year - 1
        ) // 1000 + 1

    def calculate_elapsed_time(
        self,
        start: float,
        time_unit: TimeUnit | None = None,
    ) -> float:
        if time_unit is None:
            time_unit = _TimeUnit.SECOND

        return self.convert_time_unit(
            _time.time_ns() - start,
            _TimeUnit.NANOSECOND,
            time_unit,
        )

    def calculate_duration_time(
        self,
        start: float,
        end: float,
        time_unit: TimeUnit | None = None,
    ) -> float:
        if time_unit is None:
            time_unit = _TimeUnit.SECOND

        return self.convert_time_unit(
            end - start,
            _TimeUnit.NANOSECOND,
            time_unit,
        )

    def convert_time_unit(
        self,
        value: float,
        input_time_unit: TimeUnit | None = None,
        output_time_unit: TimeUnit | None = None,
    ) -> float:
        if input_time_unit is None:
            input_time_unit = _TimeUnit.SECOND

        if output_time_unit is None:
            output_time_unit = _TimeUnit.SECOND

        if input_time_unit is output_time_unit:
            return float(value)

        nanoseconds = (
            value
            * self._TIME_UNIT_TO_NANOSECONDS[input_time_unit]
        )

        return (
            nanoseconds
            / self._TIME_UNIT_TO_NANOSECONDS[output_time_unit]
        )
