from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.log_options import (
        LogOptions,
    )

_logging: Any = None
_queue: Any = None
_QueueHandler: Any = None
_QueueListener: Any = None
_Path: Any = None
_singleton_manager: Any = None
_text_encoding_manager: Any = None
_log_format: Any = None
_log_options: Any = None
_log_options_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _logging
    global _queue
    global _QueueHandler
    global _QueueListener
    global _Path
    global _singleton_manager
    global _text_encoding_manager
    global _log_format
    global _log_options
    global _log_options_manager

    import logging
    import queue
    from logging.handlers import (
        QueueHandler,
        QueueListener,
    )
    from pathlib import Path

    import qlogicae_cor.v1.library.log_format
    import qlogicae_cor.v1.library.log_options
    import qlogicae_cor.v1.library.log_options_manager
    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.text_encoding_manager

    _logging = logging
    _queue = queue
    _QueueHandler = QueueHandler
    _QueueListener = QueueListener
    _Path = Path

    _log_format = (
        qlogicae_cor.v1.library.log_format.LogFormat
    )
    _log_options = (
        qlogicae_cor.v1.library.log_options.LogOptions
    )
    _log_options_manager = (
        qlogicae_cor.v1.library.log_options_manager.LogOptionsManager
    )

    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _text_encoding_manager = (
        qlogicae_cor.v1.library.text_encoding_manager.TextEncodingManager
    )

    _handle_dynamic_imports = lambda: None


class FileLogManager:
    __slots__ = (
        "logger",
        "file_handlers",
        "log_queue",
        "queue_handler",
        "listener",
        "_options",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self.logger = _logging.getLogger(
            "file-logger",
        )

        self.logger.setLevel(
            _logging.DEBUG,
        )

        self.logger.propagate = False

        self.logger.handlers.clear()

        self.file_handlers: Any = {}

        self.log_queue = _queue.Queue()

        self.queue_handler = _QueueHandler(
            self.log_queue,
        )

        self.logger.addHandler(
            self.queue_handler,
        )

        self.listener = _QueueListener(
            self.log_queue,
        )

        self.listener.start()

        self._options = _log_options()

    @property
    def options(self) -> LogOptions:
        value: LogOptions = self._options
        return value

    @options.setter
    def options(
        self,
        value: LogOptions,
    ) -> None:
        self._options = value

    def log(
        self,
        message: Any,
        options: LogOptions,
    ) -> Any:
        if not options.is_enabled:
            return message

        if options.is_verbose_enabled:
            self.logger.log(
                options.log_level,
                str(message).strip(),
                stacklevel=options.stack_level,
            )

        else:
            for current_file_path in self.file_handlers:
                with _Path.open(
                    current_file_path,
                    "a",
                    encoding=(
                        _singleton_manager
                        .get_singleton(
                            _text_encoding_manager,
                        )
                        .selected_encoding
                    ),
                ) as file:
                    file.write(
                        f"{str(message).strip()}\n"
                    )

        return message

    def log_debug(
        self,
        message: Any,
    ) -> Any:
        return self.log(
            message,
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                self._options,
                log_level=_logging.DEBUG,
            ),
        )

    def log_info(
        self,
        message: Any,
    ) -> Any:
        return self.log(
            message,
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                self._options,
                log_level=_logging.INFO,
            ),
        )

    def log_warning(
        self,
        message: Any,
    ) -> Any:
        return self.log(
            message,
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                self._options,
                log_level=_logging.WARNING,
            ),
        )

    def log_error(
        self,
        message: Any,
    ) -> Any:
        return self.log(
            message,
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                self._options,
                log_level=_logging.ERROR,
            ),
        )

    def log_critical(
        self,
        message: Any,
    ) -> Any:
        return self.log(
            message,
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                self._options,
                log_level=_logging.CRITICAL,
            ),
        )

    def rebuild_listener(self) -> bool:
        self.listener.stop()

        self.listener = _QueueListener(
            self.log_queue,
            *self.file_handlers.values(),
        )

        self.listener.start()

        return True

    def add_file_output(
        self,
        file_path: str,
    ) -> bool:
        path = _Path(file_path).resolve()

        if path in self.file_handlers:
            return False

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        handler = _logging.FileHandler(
            path,
            encoding=(
                _singleton_manager
                .get_singleton(
                    _text_encoding_manager,
                )
                .selected_encoding
            ),
        )

        handler.setFormatter(
            _log_format(),
        )

        self.file_handlers[path] = handler

        self.rebuild_listener()

        return True

    def remove_file_output(
        self,
        file_path: str,
    ) -> bool:
        path = _Path(file_path).resolve()

        handler = self.file_handlers.get(path)

        if handler is None:
            return False

        handler.close()

        del self.file_handlers[path]

        self.rebuild_listener()

        return True

    def clear_file_outputs(self) -> bool:
        for handler in self.file_handlers.values():
            handler.close()

        self.file_handlers.clear()

        self.rebuild_listener()

        return True

    def shutdown(self) -> bool:
        self.listener.stop()

        for handler in self.file_handlers.values():
            handler.close()

        self.file_handlers.clear()

        return True
