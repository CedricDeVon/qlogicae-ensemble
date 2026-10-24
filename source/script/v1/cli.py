from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path


def parse_bool(value: str) -> bool:
    normalized = value.lower()

    if normalized not in {"true", "false"}:
        raise argparse.ArgumentTypeError(
            "Expected 'true' or 'false'."
        )

    return normalized == "true"


def parse_key_values(values: Sequence[str]) -> dict[str, str]:
    result: dict[str, str] = {}

    for item in values:
        for entry in item.split(","):
            if "=" not in entry:
                raise ValueError(
                    f"Expected key=value, received: {entry!r}"
                )

            key, value = entry.split("=", 1)

            if not key:
                raise ValueError(
                    "Replacement keys cannot be empty."
                )

            result[key] = value

    if not result:
        raise ValueError(
            "At least one key=value pair is required."
        )

    return result


def normalize_path(value: str | Path) -> Path:
    return Path(value).resolve(strict=False)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_unprotected(
    paths: Sequence[str | Path],
    protected_paths: Sequence[str],
) -> None:
    protected = [
        normalize_path(path)
        for path in protected_paths
    ]

    for value in paths:
        path = normalize_path(value)

        for protected_path in protected:
            if (
                is_within(path, protected_path)
                or is_within(protected_path, path)
            ):
                raise PermissionError(
                    f"Operation rejected: {value!s} overlaps "
                    f"protected path {protected_path!s}."
                )


def validate_sources(
    paths: Sequence[str],
    is_required: bool,
) -> list[Path]:
    result: list[Path] = []

    for value in paths:
        path = Path(value)

        if not path.exists() and not path.is_symlink():
            if is_required:
                raise FileNotFoundError(value)
            continue

        result.append(path)

    return result


def create_filesystem_path(
    paths: Sequence[str],
    is_required: bool,
    protected_paths: Sequence[str],
) -> None:
    for value in paths:
        path = Path(value)

        if path.exists():
            if is_required:
                raise FileExistsError(value)
            continue

        validate_unprotected(
            [path],
            protected_paths,
        )

    for value in paths:
        path = Path(value)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=False)


def run_scripts(
    scripts: Sequence[str],
    is_required: bool,
) -> None:
    for script in scripts:
        path = Path(script)

        if not path.is_file():
            if is_required:
                raise FileNotFoundError(script)
            continue

        result = subprocess.run(
            [sys.executable, str(path)],
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Script failed with exit code "
                f"{result.returncode}: {script}"
            )


def remove_filesystem_path(
    paths: Sequence[str],
    is_recursive: bool,
    is_required: bool,
    protected_paths: Sequence[str],
) -> None:
    existing = validate_sources(paths, is_required)

    validate_unprotected(existing, protected_paths)

    for path in existing:
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            if is_recursive:
                shutil.rmtree(path)
            else:
                path.rmdir()
        else:
            raise OSError(
                f"Unsupported filesystem path: {path}"
            )


def rename_filesystem_path(
    source_path: str,
    target_path: str,
    is_required: bool,
    protected_paths: Sequence[str],
) -> None:
    source = Path(source_path)
    target = Path(target_path)

    if not source.exists() and not source.is_symlink():
        if is_required:
            raise FileNotFoundError(source_path)
        return

    if target.exists() or target.is_symlink():
        raise FileExistsError(target_path)

    validate_unprotected(
        [source, target],
        protected_paths,
    )

    source.rename(target)


def move_filesystem_path(
    source_path: str,
    target_path: str,
    is_required: bool,
    protected_paths: Sequence[str],
) -> None:
    source = Path(source_path)
    target = Path(target_path)

    if not source.exists() and not source.is_symlink():
        if is_required:
            raise FileNotFoundError(source_path)
        return

    if target.exists() or target.is_symlink():
        raise FileExistsError(target_path)

    validate_unprotected(
        [source, target],
        protected_paths,
    )

    shutil.move(str(source), str(target))


def copy_filesystem_paths(
    source_paths: Sequence[str],
    target_paths: Sequence[str],
    is_required: bool,
    protected_paths: Sequence[str],
) -> None:
    if len(source_paths) != len(target_paths):
        raise ValueError(
            "The number of source paths must match "
            "the number of target paths."
        )

    pairs: list[tuple[Path, Path]] = []

    for source_value, target_value in zip(
        source_paths,
        target_paths,
        strict=True,
    ):
        source = Path(source_value)
        target = Path(target_value)

        if not source.exists() and not source.is_symlink():
            if is_required:
                raise FileNotFoundError(source_value)
            continue

        if target.exists() or target.is_symlink():
            raise FileExistsError(target)

        pairs.append((source, target))

    validate_unprotected(
        [path for pair in pairs for path in pair],
        protected_paths,
    )

    for source, target in pairs:
        if source.is_symlink():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(
                source.readlink(),
                target_is_directory=source.is_dir(),
            )
        elif source.is_dir():
            shutil.copytree(source, target)
        elif source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        else:
            raise OSError(
                f"Unsupported source path: {source}"
            )


def iter_files(
    paths: Sequence[Path],
    is_recursive: bool,
    excluded_paths: Sequence[str],
    extensions: set[str],
):
    exclusions = parse_relative_exclusions(excluded_paths)

    for target in paths:
        if target.is_symlink():
            continue

        if target.is_file():
            root = target.parent.resolve()
            candidate = target.resolve()

            if is_excluded(candidate, root, exclusions):
                continue

            if not extensions or (
                target.suffix.lower() in extensions
            ):
                yield target

            continue

        if not target.is_dir():
            raise FileNotFoundError(target)

        root = target.resolve()

        def walk(directory: Path):
            try:
                entries = sorted(
                    directory.iterdir(),
                    key=lambda entry: entry.name,
                )
            except OSError:
                raise

            for entry in entries:
                if entry.is_symlink():
                    continue

                if is_excluded(entry, root, exclusions):
                    continue

                if entry.is_dir():
                    if is_recursive:
                        yield from walk(entry)
                elif entry.is_file():
                    if (
                        not extensions
                        or entry.suffix.lower() in extensions
                    ):
                        yield entry

        yield from walk(target)


def rename_filesystem_symbols(
    paths: Sequence[str],
    is_recursive: bool,
    key_values: Sequence[str],
    excluded_paths: Sequence[str],
    extensions: Sequence[str],
    is_required: bool,
    protected_paths: Sequence[str],
) -> None:
    replacements = parse_key_values(key_values)
    sources = validate_sources(paths, is_required)
    allowed_extensions = parse_extensions(extensions)

    files = list(
        iter_files(
            sources,
            is_recursive,
            excluded_paths,
            allowed_extensions,
        )
    )

    validate_unprotected(files, protected_paths)

    pattern = re.compile(
        "|".join(
            re.escape(key)
            for key in sorted(
                replacements,
                key=len,
                reverse=True,
            )
        )
    )

    def replace(match: re.Match[str]) -> str:
        return replacements[match.group(0)]

    updates: list[tuple[Path, bytes]] = []

    for path in files:
        original = path.read_bytes()

        try:
            content = original.decode("utf-8")
        except UnicodeDecodeError:
            continue

        updated = pattern.sub(replace, content)

        if updated != content:
            updates.append(
                (path, updated.encode("utf-8"))
            )

    validate_unprotected(
        [path for path, _ in updates],
        protected_paths,
    )

    for path, content in updates:
        path.write_bytes(content)



def add_common_options(
    parser: argparse.ArgumentParser,
) -> None:
    parser.add_argument(
        "-q",
        "--is-required",
        type=parse_bool,
        default=True,
        metavar="{true,false}",
        help="Fail when an input is missing; default: true.",
    )

    parser.add_argument(
        "-p",
        "--non-deletable-path",
        dest="protected_paths",
        action="append",
        default=[],
        metavar="PATH",
        help=(
            "Protect a path and its descendants. "
            "Repeat to protect multiple paths."
        ),
    )



def parse_extensions(values: Sequence[str]) -> set[str]:
    extensions: set[str] = set()

    for value in values:
        for extension in value.split(","):
            extension = extension.strip().lower()

            if not extension:
                continue

            if extension.startswith("*."):
                extension = extension[1:]
            elif not extension.startswith("."):
                extension = f".{extension}"

            if extension == ".":
                raise ValueError(
                    "File extensions must not be empty."
                )

            extensions.add(extension)

    return extensions


def parse_relative_exclusions(
    values: Sequence[str],
) -> tuple[Path, ...]:
    exclusions: list[Path] = []

    for value in values:
        normalized = value.replace("\\", "/")
        relative = Path(normalized)

        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(
                f"Exclusion must be a relative path "
                f"without '..': {value!r}"
            )

        exclusions.append(relative)

    return tuple(exclusions)


def is_excluded(
    path: Path,
    root: Path,
    exclusions: Sequence[Path],
) -> bool:
    relative = path.resolve().relative_to(root.resolve())

    return any(
        relative == exclusion
        or exclusion in relative.parents
        for exclusion in exclusions
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="filesystem-cli",
        description="Cross-platform filesystem utilities.",
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    create = commands.add_parser(
        "create-filesystem-path",
        aliases=["mk"],
    )
    add_common_options(create)
    create.add_argument("paths", nargs="+")

    run = commands.add_parser(
        "run-script",
        aliases=["run"],
    )
    add_common_options(run)
    run.add_argument("scripts", nargs="+")

    remove = commands.add_parser(
        "remove-filesystem-path",
        aliases=["rm"],
    )
    add_common_options(remove)
    remove.add_argument(
        "-r",
        "--is-recursive",
        type=parse_bool,
        default=False,
        metavar="{true,false}",
    )
    remove.add_argument("paths", nargs="+")

    rename = commands.add_parser(
        "rename-filesystem-path",
        aliases=["ren"],
    )
    add_common_options(rename)
    rename.add_argument("-s", "--source-path", required=True)
    rename.add_argument("-t", "--target-path", required=True)

    move = commands.add_parser(
        "move-filesystem-path",
        aliases=["mv"],
    )
    add_common_options(move)
    move.add_argument("-s", "--source-path", required=True)
    move.add_argument("-t", "--target-path", required=True)

    copy = commands.add_parser(
        "copy-filesystem-path",
        aliases=["cp"],
    )
    add_common_options(copy)
    copy.add_argument(
        "-s",
        "--source-paths",
        nargs="+",
        required=True,
    )
    copy.add_argument(
        "-t",
        "--target-paths",
        nargs="+",
        required=True,
    )
        
    symbols = commands.add_parser(
        "rename-filesystem-symbols",
        aliases=["sym"],
    )
    add_common_options(symbols)

    symbols.add_argument(
        "-r",
        "--is-recursive",
        type=parse_bool,
        default=False,
        metavar="{true,false}",
    )

    symbols.add_argument(
        "-k",
        "--key-value",
        action="append",
        required=True,
        metavar="KEY=VALUE",
        help=(
            "Literal replacement pair. Repeat for additional pairs; "
            "comma-separated pairs are also supported."
        ),
    )

    symbols.add_argument(
        "-e",
        "--exclude",
        dest="excluded_paths",
        action="append",
        default=[],
        metavar="RELATIVE_PATH",
        help=(
            "Relative file or directory to exclude. "
            "Repeat this option for multiple exclusions."
        ),
    )

    symbols.add_argument(
        "-x",
        "--extensions",
        action="append",
        default=[],
        metavar="EXTENSION",
        help=(
            "Included file extension, such as .py. "
            "Repeat this option or use comma-separated extensions."
        ),
    )

    symbols.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Target files or directories; defaults to the current directory.",
    )


    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command in {
            "create-filesystem-path",
            "mk",
        }:
            create_filesystem_path(
                args.paths,
                args.is_required,
                args.protected_paths,
            )

        elif args.command in {"run-script", "run"}:
            run_scripts(
                args.scripts,
                args.is_required,
            )

        elif args.command in {
            "remove-filesystem-path",
            "rm",
        }:
            remove_filesystem_path(
                args.paths,
                args.is_recursive,
                args.is_required,
                args.protected_paths,
            )

        elif args.command in {
            "rename-filesystem-path",
            "ren",
        }:
            rename_filesystem_path(
                args.source_path,
                args.target_path,
                args.is_required,
                args.protected_paths,
            )

        elif args.command in {
            "move-filesystem-path",
            "mv",
        }:
            move_filesystem_path(
                args.source_path,
                args.target_path,
                args.is_required,
                args.protected_paths,
            )

        elif args.command in {
            "copy-filesystem-path",
            "cp",
        }:
            copy_filesystem_paths(
                args.source_paths,
                args.target_paths,
                args.is_required,
                args.protected_paths,
            )
                
        elif args.command in {
            "rename-filesystem-symbols",
            "sym",
        }:
            rename_filesystem_symbols(
                args.paths or ["."],
                args.is_recursive,
                args.key_value,
                args.excluded_paths,
                args.extensions,
                args.is_required,
                args.protected_paths,
            )


        return 0

    except (OSError, ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
