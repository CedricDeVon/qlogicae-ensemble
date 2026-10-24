from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from .. import cli


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def protected_file(workspace: Path) -> Path:
    path = workspace / "protected.txt"
    path.write_text("protected", encoding="utf-8")
    return path


def test_parse_bool_accepts_true_and_false() -> None:
    assert cli.parse_bool("true") is True
    assert cli.parse_bool("false") is False
    assert cli.parse_bool("TRUE") is True
    assert cli.parse_bool("FALSE") is False


@pytest.mark.parametrize("value", ["yes", "no", "1", "0", ""])
def test_parse_bool_rejects_invalid_values(value: str) -> None:
    with pytest.raises(cli.argparse.ArgumentTypeError):
        cli.parse_bool(value)


def test_parse_key_values_supports_repeated_and_comma_separated_pairs() -> None:
    result = cli.parse_key_values(
        ["old=new", "first=second,third=fourth"]
    )

    assert result == {
        "old": "new",
        "first": "second",
        "third": "fourth",
    }


def test_parse_key_values_allows_equals_in_replacement_value() -> None:
    assert cli.parse_key_values(["old=a=b"]) == {"old": "a=b"}


@pytest.mark.parametrize(
    "values",
    [
        [],
        ["invalid"],
        ["=replacement"],
        ["valid=replacement", "invalid"],
    ],
)
def test_parse_key_values_rejects_invalid_pairs(
    values: list[str],
) -> None:
    with pytest.raises(ValueError):
        cli.parse_key_values(values)


def test_normalize_path_returns_absolute_path(
    workspace: Path,
) -> None:
    path = cli.normalize_path(workspace / "file.txt")

    assert path.is_absolute()
    assert path == workspace / "file.txt"


def test_is_within_accepts_same_path_and_descendants(
    workspace: Path,
) -> None:
    parent = workspace / "parent"

    assert cli.is_within(parent, parent)
    assert cli.is_within(parent / "child.txt", parent)


def test_is_within_rejects_unrelated_path(
    workspace: Path,
) -> None:
    assert not cli.is_within(
        workspace / "first",
        workspace / "second",
    )


def test_validate_unprotected_accepts_unprotected_path(
    workspace: Path,
) -> None:
    cli.validate_unprotected(
        [workspace / "ordinary.txt"],
        [str(workspace / "protected")],
    )


@pytest.mark.parametrize(
    ("target", "protected"),
    [
        ("protected.txt", "protected.txt"),
        ("protected/child.txt", "protected"),
        ("protected", "protected/child.txt"),
    ],
)
def test_validate_unprotected_rejects_overlapping_paths(
    workspace: Path,
    target: str,
    protected: str,
) -> None:
    with pytest.raises(PermissionError):
        cli.validate_unprotected(
            [workspace / target],
            [str(workspace / protected)],
        )


def test_validate_sources_returns_existing_paths(
    workspace: Path,
) -> None:
    path = workspace / "file.txt"
    path.write_text("content", encoding="utf-8")

    assert cli.validate_sources([str(path)], True) == [path]


def test_validate_sources_raises_for_missing_required_path(
    workspace: Path,
) -> None:
    missing = workspace / "missing.txt"

    with pytest.raises(FileNotFoundError):
        cli.validate_sources([str(missing)], True)


def test_validate_sources_skips_missing_optional_path(
    workspace: Path,
) -> None:
    existing = workspace / "existing.txt"
    existing.write_text("content", encoding="utf-8")

    result = cli.validate_sources(
        [str(existing), str(workspace / "missing.txt")],
        False,
    )

    assert result == [existing]


def test_create_filesystem_path_creates_nested_directories(
    workspace: Path,
) -> None:
    target = workspace / "one" / "two" / "three"

    cli.create_filesystem_path([str(target)], True, [])

    assert target.is_dir()


def test_create_filesystem_path_rejects_existing_path(
    workspace: Path,
) -> None:
    target = workspace / "existing"
    target.mkdir()

    with pytest.raises(FileExistsError):
        cli.create_filesystem_path([str(target)], True, [])


def test_create_filesystem_path_skips_existing_optional_path(
    workspace: Path,
) -> None:
    target = workspace / "existing"
    target.mkdir()

    cli.create_filesystem_path([str(target)], False, [])

    assert target.is_dir()


def test_create_filesystem_path_rejects_protected_path(
    workspace: Path,
) -> None:
    target = workspace / "protected"

    with pytest.raises(PermissionError):
        cli.create_filesystem_path(
            [str(target)],
            True,
            [str(target)],
        )

    assert not target.exists()


def test_run_scripts_executes_python_script(
    workspace: Path,
) -> None:
    output = workspace / "output.txt"
    script = workspace / "script.py"
    script.write_text(
        "from pathlib import Path\n"
        f"Path({str(output)!r}).write_text('success', encoding='utf-8')\n",
        encoding="utf-8",
    )

    cli.run_scripts([str(script)], True)

    assert output.read_text(encoding="utf-8") == "success"


def test_run_scripts_rejects_missing_required_script(
    workspace: Path,
) -> None:
    with pytest.raises(FileNotFoundError):
        cli.run_scripts([str(workspace / "missing.py")], True)


def test_run_scripts_skips_missing_optional_script(
    workspace: Path,
) -> None:
    cli.run_scripts([str(workspace / "missing.py")], False)


def test_run_scripts_raises_when_script_fails(
    workspace: Path,
) -> None:
    script = workspace / "failure.py"
    script.write_text("raise SystemExit(7)\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="exit code 7"):
        cli.run_scripts([str(script)], True)


def test_remove_filesystem_path_removes_file(
    workspace: Path,
) -> None:
    target = workspace / "file.txt"
    target.write_text("content", encoding="utf-8")

    cli.remove_filesystem_path([str(target)], False, True, [])

    assert not target.exists()


def test_remove_filesystem_path_removes_empty_directory(
    workspace: Path,
) -> None:
    target = workspace / "empty"
    target.mkdir()

    cli.remove_filesystem_path([str(target)], False, True, [])

    assert not target.exists()


def test_remove_filesystem_path_requires_recursive_for_nonempty_directory(
    workspace: Path,
) -> None:
    target = workspace / "directory"
    target.mkdir()
    (target / "file.txt").write_text("content", encoding="utf-8")

    with pytest.raises(OSError):
        cli.remove_filesystem_path([str(target)], False, True, [])

    assert target.is_dir()


def test_remove_filesystem_path_removes_directory_recursively(
    workspace: Path,
) -> None:
    target = workspace / "directory"
    target.mkdir()
    (target / "file.txt").write_text("content", encoding="utf-8")

    cli.remove_filesystem_path([str(target)], True, True, [])

    assert not target.exists()


def test_remove_filesystem_path_skips_missing_optional_path(
    workspace: Path,
) -> None:
    cli.remove_filesystem_path(
        [str(workspace / "missing")],
        False,
        False,
        [],
    )


def test_remove_filesystem_path_rejects_protected_file(
    protected_file: Path,
) -> None:
    with pytest.raises(PermissionError):
        cli.remove_filesystem_path(
            [str(protected_file)],
            False,
            True,
            [str(protected_file)],
        )

    assert protected_file.exists()


def test_rename_filesystem_path_renames_file(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "target.txt"
    source.write_text("content", encoding="utf-8")

    cli.rename_filesystem_path(
        str(source),
        str(target),
        True,
        [],
    )

    assert not source.exists()
    assert target.read_text(encoding="utf-8") == "content"


def test_rename_filesystem_path_rejects_existing_target(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "target.txt"
    source.write_text("source", encoding="utf-8")
    target.write_text("target", encoding="utf-8")

    with pytest.raises(FileExistsError):
        cli.rename_filesystem_path(
            str(source),
            str(target),
            True,
            [],
        )

    assert source.exists()
    assert target.read_text(encoding="utf-8") == "target"


def test_rename_filesystem_path_rejects_protected_source(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "target.txt"
    source.write_text("content", encoding="utf-8")

    with pytest.raises(PermissionError):
        cli.rename_filesystem_path(
            str(source),
            str(target),
            True,
            [str(source)],
        )

    assert source.exists()
    assert not target.exists()


def test_move_filesystem_path_moves_file(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "target.txt"
    source.write_text("content", encoding="utf-8")

    cli.move_filesystem_path(
        str(source),
        str(target),
        True,
        [],
    )

    assert not source.exists()
    assert target.read_text(encoding="utf-8") == "content"


def test_move_filesystem_path_rejects_existing_target(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "target.txt"
    source.write_text("source", encoding="utf-8")
    target.write_text("target", encoding="utf-8")

    with pytest.raises(FileExistsError):
        cli.move_filesystem_path(
            str(source),
            str(target),
            True,
            [],
        )

    assert source.exists()


def test_copy_filesystem_paths_copies_files(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "nested" / "target.txt"
    source.write_text("content", encoding="utf-8")

    cli.copy_filesystem_paths(
        [str(source)],
        [str(target)],
        True,
        [],
    )

    assert source.read_text(encoding="utf-8") == "content"
    assert target.read_text(encoding="utf-8") == "content"


def test_copy_filesystem_paths_copies_directories(
    workspace: Path,
) -> None:
    source = workspace / "source"
    source.mkdir()
    (source / "file.txt").write_text("content", encoding="utf-8")
    target = workspace / "target"

    cli.copy_filesystem_paths(
        [str(source)],
        [str(target)],
        True,
        [],
    )

    assert (source / "file.txt").read_text(encoding="utf-8") == "content"
    assert (target / "file.txt").read_text(encoding="utf-8") == "content"


def test_copy_filesystem_paths_rejects_mismatched_lengths(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    source.write_text("content", encoding="utf-8")

    with pytest.raises(ValueError, match="must match"):
        cli.copy_filesystem_paths(
            [str(source)],
            [str(workspace / "first"), str(workspace / "second")],
            True,
            [],
        )


def test_copy_filesystem_paths_rejects_existing_target(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "target.txt"
    source.write_text("source", encoding="utf-8")
    target.write_text("target", encoding="utf-8")

    with pytest.raises(FileExistsError):
        cli.copy_filesystem_paths(
            [str(source)],
            [str(target)],
            True,
            [],
        )


def test_copy_filesystem_paths_rejects_protected_target(
    workspace: Path,
) -> None:
    source = workspace / "source.txt"
    target = workspace / "protected.txt"
    source.write_text("content", encoding="utf-8")

    with pytest.raises(PermissionError):
        cli.copy_filesystem_paths(
            [str(source)],
            [str(target)],
            True,
            [str(target)],
        )

    assert source.exists()
    assert not target.exists()


def test_parse_extensions_normalizes_values() -> None:
    assert cli.parse_extensions(
        [".PY,py", "*.TOML", "yaml"]
    ) == {".py", ".toml", ".yaml"}


def test_parse_extensions_ignores_empty_values() -> None:
    assert cli.parse_extensions(["", ","]) == set()


def test_parse_relative_exclusions_normalizes_separators() -> None:
    assert cli.parse_relative_exclusions(
        ["generated\\cache", "tests/fixtures"]
    ) == (
        Path("generated/cache"),
        Path("tests/fixtures"),
    )


@pytest.mark.parametrize(
    "value",
    [
        "/absolute/path",
        "../outside",
        "nested/../../outside",
    ],
)
def test_parse_relative_exclusions_rejects_unsafe_paths(
    value: str,
) -> None:
    with pytest.raises(ValueError):
        cli.parse_relative_exclusions([value])


def test_is_excluded_matches_exact_path_and_descendants(
    workspace: Path,
) -> None:
    root = workspace / "project"
    exclusions = (Path("generated"), Path("tests/fixtures"))

    assert cli.is_excluded(
        root / "generated",
        root,
        exclusions,
    )
    assert cli.is_excluded(
        root / "generated" / "file.py",
        root,
        exclusions,
    )
    assert cli.is_excluded(
        root / "tests" / "fixtures" / "case.py",
        root,
        exclusions,
    )
    assert not cli.is_excluded(
        root / "src" / "main.py",
        root,
        exclusions,
    )


def test_iter_files_filters_extensions_and_exclusions(
    workspace: Path,
) -> None:
    root = workspace / "project"
    (root / "src").mkdir(parents=True)
    (root / "generated").mkdir()

    (root / "src" / "main.py").write_text("old", encoding="utf-8")
    (root / "src" / "data.toml").write_text("old", encoding="utf-8")
    (root / "generated" / "build.py").write_text(
        "old",
        encoding="utf-8",
    )

    files = list(
        cli.iter_files(
            [root],
            True,
            ["generated"],
            {".py"},
        )
    )

    assert files == [root / "src" / "main.py"]


def test_iter_files_does_not_descend_without_recursion(
    workspace: Path,
) -> None:
    root = workspace / "project"
    nested = root / "nested"
    nested.mkdir(parents=True)
    (root / "root.py").write_text("old", encoding="utf-8")
    (nested / "nested.py").write_text("old", encoding="utf-8")

    files = list(
        cli.iter_files([root], False, [], {".py"})
    )

    assert files == [root / "root.py"]


def test_iter_files_accepts_a_single_file(
    workspace: Path,
) -> None:
    target = workspace / "main.py"
    target.write_text("old", encoding="utf-8")

    assert list(
        cli.iter_files([target], False, [], {".py"})
    ) == [target]


def test_rename_filesystem_symbols_replaces_literals(
    workspace: Path,
) -> None:
    target = workspace / "main.py"
    target.write_text(
        "old_name old old_name\n",
        encoding="utf-8",
    )

    cli.rename_filesystem_symbols(
        [str(target)],
        False,
        ["old_name=new_name", "old=new"],
        [],
        [".py"],
        True,
        [],
    )

    assert target.read_text(encoding="utf-8") == (
        "new_name new new_name\n"
    )


def test_rename_filesystem_symbols_supports_recursive_directories(
    workspace: Path,
) -> None:
    root = workspace / "project"
    nested = root / "nested"
    nested.mkdir(parents=True)

    top_file = root / "main.py"
    nested_file = nested / "module.py"
    top_file.write_text("old", encoding="utf-8")
    nested_file.write_text("old", encoding="utf-8")

    cli.rename_filesystem_symbols(
        [str(root)],
        True,
        ["old=new"],
        [],
        [".py"],
        True,
        [],
    )

    assert top_file.read_text(encoding="utf-8") == "new"
    assert nested_file.read_text(encoding="utf-8") == "new"


def test_rename_filesystem_symbols_excludes_relative_paths(
    workspace: Path,
) -> None:
    root = workspace / "project"
    source = root / "src"
    excluded = root / "generated"
    source.mkdir(parents=True)
    excluded.mkdir()

    included_file = source / "main.py"
    excluded_file = excluded / "build.py"
    included_file.write_text("old", encoding="utf-8")
    excluded_file.write_text("old", encoding="utf-8")

    cli.rename_filesystem_symbols(
        [str(root)],
        True,
        ["old=new"],
        ["generated"],
        [".py"],
        True,
        [],
    )

    assert included_file.read_text(encoding="utf-8") == "new"
    assert excluded_file.read_text(encoding="utf-8") == "old"


def test_rename_filesystem_symbols_filters_extensions(
    workspace: Path,
) -> None:
    root = workspace / "project"
    root.mkdir()

    python_file = root / "main.py"
    toml_file = root / "config.toml"
    python_file.write_text("old", encoding="utf-8")
    toml_file.write_text("old", encoding="utf-8")

    cli.rename_filesystem_symbols(
        [str(root)],
        False,
        ["old=new"],
        [],
        [".py"],
        True,
        [],
    )

    assert python_file.read_text(encoding="utf-8") == "new"
    assert toml_file.read_text(encoding="utf-8") == "old"


def test_rename_filesystem_symbols_skips_binary_files(
    workspace: Path,
) -> None:
    target = workspace / "data.bin"
    original = b"\xff\xfe\x00old"

    target.write_bytes(original)

    cli.rename_filesystem_symbols(
        [str(target)],
        False,
        ["old=new"],
        [],
        [],
        True,
        [],
    )

    assert target.read_bytes() == original


def test_rename_filesystem_symbols_rejects_protected_file(
    workspace: Path,
) -> None:
    target = workspace / "main.py"
    target.write_text("old", encoding="utf-8")

    with pytest.raises(PermissionError):
        cli.rename_filesystem_symbols(
            [str(target)],
            False,
            ["old=new"],
            [],
            [".py"],
            True,
            [str(target)],
        )

    assert target.read_text(encoding="utf-8") == "old"


def test_rename_filesystem_symbols_skips_missing_optional_path(
    workspace: Path,
) -> None:
    cli.rename_filesystem_symbols(
        [str(workspace / "missing.py")],
        False,
        ["old=new"],
        [],
        [".py"],
        False,
        [],
    )


def test_build_parser_supports_short_aliases() -> None:
    parser = cli.build_parser()

    assert parser.parse_args(["mk", "directory"]).command == "mk"
    assert parser.parse_args(["run", "script.py"]).command == "run"
    assert parser.parse_args(["rm", "file.txt"]).command == "rm"
    assert parser.parse_args(
        ["ren", "-s", "a", "-t", "b"]
    ).command == "ren"
    assert parser.parse_args(
        ["mv", "-s", "a", "-t", "b"]
    ).command == "mv"
    assert parser.parse_args(
        ["cp", "-s", "a", "-t", "b"]
    ).command == "cp"


def test_build_parser_defaults_symbols_target_to_current_directory() -> None:
    args = cli.build_parser().parse_args(
        ["sym", "-k", "old=new"]
    )

    assert args.paths == ["."]
    assert args.is_recursive is False
    assert args.is_required is True
    assert args.excluded_paths == []
    assert args.extensions == []


def test_build_parser_supports_multiple_symbol_options() -> None:
    args = cli.build_parser().parse_args(
        [
            "sym",
            "-k",
            "old=new",
            "-k",
            "first=second,third=fourth",
            "-e",
            "generated",
            "-e",
            "tests/fixtures",
            "-x",
            ".py,.toml",
            "src",
        ]
    )

    assert args.key_value == [
        "old=new",
        "first=second,third=fourth",
    ]
    assert args.excluded_paths == [
        "generated",
        "tests/fixtures",
    ]
    assert args.extensions == [".py,.toml"]
    assert args.paths == ["src"]


def test_main_symbol_command_returns_success(
    workspace: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target = workspace / "main.py"
    target.write_text("old", encoding="utf-8")

    result = cli.main(
        [
            "sym",
            "-k",
            "old=new",
            "-x",
            ".py",
            str(target),
        ]
    )

    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == ""
    assert captured.err == ""
    assert target.read_text(encoding="utf-8") == "new"


def test_main_returns_error_for_missing_required_path(
    workspace: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = cli.main(
        [
            "sym",
            "-k",
            "old=new",
            str(workspace / "missing.py"),
        ]
    )

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == ""
    assert "error:" in captured.err
    assert "missing.py" in captured.err


def test_main_allows_missing_optional_symbol_path(
    workspace: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = cli.main(
        [
            "sym",
            "-q",
            "false",
            "-k",
            "old=new",
            str(workspace / "missing.py"),
        ]
    )

    captured = capsys.readouterr()

    assert result == 0
    assert captured.err == ""


def test_main_rejects_protected_symbol_path(
    workspace: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target = workspace / "protected.py"
    target.write_text("old", encoding="utf-8")

    result = cli.main(
        [
            "sym",
            "-k",
            "old=new",
            "-p",
            str(target),
            str(target),
        ]
    )

    captured = capsys.readouterr()

    assert result == 1
    assert "error:" in captured.err
    assert target.read_text(encoding="utf-8") == "old"
