from __future__ import annotations

from typing import Any, cast

_figlet: Any = None
_console: Any = None
_padding: Any = None
_progress: Any = None
_rule: Any = None
_table: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _figlet
    global _console
    global _padding
    global _progress
    global _rule
    global _table

    import pyfiglet
    import rich.console
    import rich.padding
    import rich.progress
    import rich.rule
    import rich.table

    _figlet = pyfiglet.Figlet
    _console = rich.console.Console
    _padding = rich.padding.Padding
    _progress = rich.progress
    _rule = rich.rule.Rule
    _table = rich.table.Table

    _handle_dynamic_imports = lambda: None


class ConsoleComponentManager:
    __slots__ = ("_console",)

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._console: _console = _console()

    @property
    def console(self) -> Any:
        return self._console

    @property
    def table(self) -> Any:
        return _table(
            show_header=False,
            box=None,
            pad_edge=False,
            padding=(0, 4, 1, 4),
        )

    @property
    def progress_bar(self) -> Any:
        return _progress.Progress(
            _progress.SpinnerColumn(
                "dots",
                style="bold bright_green",
            ),
            _progress.TextColumn(
                "[green]{task.description}",
            ),
            _progress.BarColumn(
                bar_width=80,
                complete_style="green",
            ),
            _progress.TextColumn(
                "[green]{task.percentage:>6.2f}%",
            ),
            _progress.TimeElapsedColumn(),
        )

    def setup_table(
        self,
        data: dict[str, object] | None = None,
    ) -> Any:
        if not data:
            return self.setup_padding()

        cli_table = self.table

        cli_table_headers = cast(
            list[dict[str, object]],
            data.get("headers", []),
        )

        for cli_table_header in cli_table_headers:
            cli_table_header_name = (
                cli_table_header["name"] if "name" in cli_table_header else "name"
            )
            cli_table_header_style = (
                cli_table_header["style"] if "style" in cli_table_header else "white"
            )
            cli_table_header_no_wrap = (
                cli_table_header["no_wrap"] if "no_wrap" in cli_table_header else True
            )

            cli_table.add_column(
                cli_table_header_name,
                style=cli_table_header_style,
                no_wrap=cli_table_header_no_wrap,
            )

        cli_table_rows = cast(
            list[list[str]],
            data.get("rows", []),
        )

        for cli_table_row in cli_table_rows:
            cli_table.add_row(
                *cli_table_row,
            )

        return self.setup_padding(
            cli_table,
        )

    def setup_horizontal_rule(
        self,
    ) -> Any:
        result: _padding = _padding(
            _rule(
                style="bold green",
            ),
            (0, 2),
        )

        return result

    def setup_branding(
        self,
        brand_name: str,
        brand_description: str,
    ) -> Any:
        brand_name = (
            brand_name
            or "Brand"
        )

        brand_description = (
            brand_description
            or "Description"
        )

        return self.setup_padding(
            f"[white]{_figlet(font='slant').renderText(brand_name)}[/]\n"
            f"[white]{brand_description}[/]",
        )

    def setup_duration_text(
        self,
        text: str = "",
    ) -> Any:
        return self.setup_padding(
            f"[dim]{text} seconds[/]",
        )

    def setup_end_padding(
        self,
    ) -> Any:
        return self.setup_padding(
            "",
            0,
            4,
        )

    def setup_padding(
        self,
        text: Any = "",
        vertical: int = 1,
        horizontal: int = 4,
    ) -> Any:
        result: _padding = _padding(
            text,
            (
                vertical,
                horizontal,
            ),
        )

        return result
