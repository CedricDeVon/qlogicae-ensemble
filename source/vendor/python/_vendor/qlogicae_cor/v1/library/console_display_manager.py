from __future__ import annotations

from typing import Any, cast

_time: Any = None
_live: Any = None
_console_component_manager: Any = None
_singleton_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _time
    global _live
    global _console_component_manager
    global _singleton_manager

    import time

    from rich.live import Live

    import qlogicae_cor.v1.library.console_component_manager
    import qlogicae_cor.v1.library.singleton_manager

    _time = time
    _live = Live
    _console_component_manager = (
        qlogicae_cor.v1.library.console_component_manager.ConsoleComponentManager
    )
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )

    _handle_dynamic_imports = lambda: None


class ConsoleDisplayManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def render_directly(
        self,
        data: dict[str, object] | None = None,
    ) -> bool:
        if not data:
            return False

        progress_items = cast(
            list[dict[str, object]],
            data.get("items", []),
        )

        for task in progress_items:
            task_callback = task.get("callback")
            task_arguments = cast(
                dict[str, object],
                task.get("arguments", {}),
            )
            task_delay = cast(
                dict[str, object],
                task.get("delay", {}),
            )
            task_delay_in_seconds = cast(
                float,
                task_delay.get("value", 0),
            )

            if task_delay_in_seconds:
                _time.sleep(task_delay_in_seconds)

            if callable(task_callback):
                task_callback(**task_arguments)

        return True

    def render_progress_bar(
        self,
        data: dict[str, object] | None = None,
    ) -> bool:
        if not data:
            return False

        progress_bar = (
            _singleton_manager.get_singleton(
                _console_component_manager,
            ).progress_bar
        )

        progress_bar_task = progress_bar.add_task(
            "",
            total=100,
        )

        progress_items = cast(
            list[dict[str, object]],
            data.get("items", []),
        )
        progress_refresh = cast(
            dict[str, object],
            data.get("refresh", {}),
        )
        progress_refresh_value = cast(
            int,
            progress_refresh.get("value", 60),
        )
        progress_transient = cast(
            dict[str, object],
            data.get("transient", {}),
        )
        progress_transient_value = cast(
            bool,
            progress_transient.get("value", True),
        )

        live: _live = _live(
            progress_bar,
            console=_singleton_manager.get_singleton(
                _console_component_manager,
            ).console,
            refresh_per_second=progress_refresh_value,
            transient=progress_transient_value,
        )

        with live:
            time_start = _time.perf_counter()

            for index, task in enumerate(progress_items):
                task_message = cast(
                    str,
                    task.get("message", "Loading"),
                )
                task_callback = task.get("callback")
                task_arguments = cast(
                    dict[str, object],
                    task.get("arguments", {}),
                )
                task_delay = cast(
                    dict[str, object],
                    task.get("delay", {}),
                )
                task_delay_in_seconds = cast(
                    float,
                    task_delay.get("value", 0),
                )

                progress_bar.update(
                    progress_bar_task,
                    description=task_message,
                )

                if task_delay_in_seconds:
                    _time.sleep(task_delay_in_seconds)

                if callable(task_callback):
                    task_callback(**task_arguments)

                progress_bar.update(
                    progress_bar_task,
                    completed=min(
                        (index + 1)
                        / len(progress_items)
                        * 100,
                        100,
                    ),
                    elapsed=(
                        f"{_time.perf_counter() - time_start:.2f}s"
                    ),
                )

        return True

    def render_one_component(
        self,
        content: Any,
    ) -> bool:
        _singleton_manager.get_singleton(
            _console_component_manager,
        ).console.print(content)

        return True

    def render_many_components(
        self,
        items: list[object] | None = None,
    ) -> bool:
        if not items:
            return False

        for item in items:
            if not item:
                return False

            self.render_one_component(
                item,
            )

        return True
