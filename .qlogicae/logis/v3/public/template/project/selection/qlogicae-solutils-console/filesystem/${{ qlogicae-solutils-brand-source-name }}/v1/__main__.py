from __future__ import annotations


def main() -> int:
    try:
        import sys
        import subprocess
        from pathlib import Path

        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve().parent / "app.py"),
                *sys.argv[1:],
            ],
            check=False,
            shell=False,
        )

        return result.returncode

    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
