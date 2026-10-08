from __future__ import annotations

__all__ = (
    "AsynchronousManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import asyncio
    import threading
    from collections.abc import (
        Callable,
        Coroutine,
        Iterable,
    )
    from concurrent.futures import (
        ProcessPoolExecutor,
        ThreadPoolExecutor,
    )
    from typing import ParamSpec, TypeVar

    P = ParamSpec("P")
    T = TypeVar("T")

_asyncio: Any = None
_threading: Any = None
_partial: Any = None
_ProcessPoolExecutor: Any = None
_ThreadPoolExecutor: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _asyncio
    global _threading
    global _partial
    global _ProcessPoolExecutor
    global _ThreadPoolExecutor

    import asyncio
    import threading
    from concurrent.futures import (
        ProcessPoolExecutor,
        ThreadPoolExecutor,
    )
    from functools import partial

    _asyncio = asyncio
    _threading = threading
    _partial = partial
    _ProcessPoolExecutor = ProcessPoolExecutor
    _ThreadPoolExecutor = ThreadPoolExecutor

    _handle_dynamic_imports = lambda: None


class AsynchronousManager:
    __slots__ = (
        "_thread_executor",
        "_process_executor",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._thread_executor: (
            ThreadPoolExecutor | None
        ) = None

        self._process_executor: (
            ProcessPoolExecutor | None
        ) = None

    @property
    def thread_executor(
        self,
    ) -> ThreadPoolExecutor:
        if self._thread_executor is None:
            self._thread_executor = (
                _ThreadPoolExecutor()
            )

        return self._thread_executor

    @property
    def process_executor(
        self,
    ) -> ProcessPoolExecutor:
        if self._process_executor is None:
            self._process_executor = (
                _ProcessPoolExecutor()
            )

        return self._process_executor

    async def run_thread(
        self,
        function: Callable[P, T],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        result: T = await _asyncio.to_thread(
            function,
            *args,
            **kwargs,
        )

        return result

    async def run_thread_pool(
        self,
        function: Callable[P, T],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        loop = _asyncio.get_running_loop()

        result: T = await loop.run_in_executor(
            self.thread_executor,
            _partial(
                function,
                *args,
                **kwargs,
            ),
        )

        return result

    async def run_process_pool(
        self,
        function: Callable[P, T],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        loop = _asyncio.get_running_loop()

        result: T = await loop.run_in_executor(
            self.process_executor,
            _partial(
                function,
                *args,
                **kwargs,
            ),
        )

        return result

    async def gather(
        self,
        *coroutines: Coroutine[Any, Any, Any],
        return_exceptions: bool = False,
    ) -> list[Any]:
        result: list[Any] = await _asyncio.gather(
            *coroutines,
            return_exceptions=return_exceptions,
        )

        return result

    async def wait(
        self,
        *coroutines: Coroutine[Any, Any, Any],
        timeout: float | None = None,
    ) -> tuple[
        set[asyncio.Task[Any]],
        set[asyncio.Task[Any]],
    ]:
        tasks: set[Any] = {
            _asyncio.create_task(coroutine)
            for coroutine in coroutines
        }

        result: tuple[
            set[asyncio.Task[Any]],
            set[asyncio.Task[Any]],
        ] = await _asyncio.wait(
            tasks,
            timeout=timeout,
        )

        return result

    def create_task(
        self,
        coroutine: Coroutine[Any, Any, T],
        name: str | None = None,
    ) -> asyncio.Task[T]:
        result: asyncio.Task[T] = _asyncio.create_task(
            coroutine,
            name=name,
        )

        return result

    async def timeout(
        self,
        coroutine: Coroutine[Any, Any, T],
        seconds: float,
    ) -> T:
        result: T = await _asyncio.wait_for(
            coroutine,
            timeout=seconds,
        )

        return result

    async def map_thread(
        self,
        function: Callable[..., T],
        *iterables: Iterable[Any],
    ) -> list[T]:
        result: list[T] = await _asyncio.gather(
            *(
                self.run_thread(
                    function,
                    *values,
                )
                for values in zip(
                    *iterables,
                    strict=True,
                )
            )
        )

        return result

    async def map_thread_pool(
        self,
        function: Callable[..., T],
        *iterables: Iterable[Any],
    ) -> list[T]:
        result: list[T] = await _asyncio.gather(
            *(
                self.run_thread_pool(
                    function,
                    *values,
                )
                for values in zip(
                    *iterables,
                    strict=True,
                )
            )
        )

        return result

    async def map_process_pool(
        self,
        function: Callable[..., T],
        *iterables: Iterable[Any],
    ) -> list[T]:
        result: list[T] = await _asyncio.gather(
            *(
                self.run_process_pool(
                    function,
                    *values,
                )
                for values in zip(
                    *iterables,
                    strict=True,
                )
            )
        )

        return result

    def create_thread(
        self,
        function: Callable[..., Any],
        /,
        *args: Any,
        daemon: bool = False,
        start: bool = True,
        **kwargs: Any,
    ) -> threading.Thread:
        thread: threading.Thread = _threading.Thread(
            target=function,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
        )

        if start:
            thread.start()

        return thread

    def shutdown(
        self,
        *,
        wait: bool = True,
    ) -> None:
        if self._thread_executor is not None:
            self._thread_executor.shutdown(
                wait=wait,
            )

            self._thread_executor = None

        if self._process_executor is not None:
            self._process_executor.shutdown(
                wait=wait,
            )

            self._process_executor = None

    def __enter__(
        self,
    ) -> AsynchronousManager:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: Any,
    ) -> None:
        self.shutdown()
